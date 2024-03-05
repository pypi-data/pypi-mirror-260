import io
import time
from pathlib import Path

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.base import File as DjangoFile
from django_clamd.validators import validate_file_infection
from manabi import ManabiAuthenticator, ManabiDAVApp
from manabi.filesystem import ManabiFileResourceMixin, ManabiProvider
from manabi.lock import ManabiDbLockStorage
from manabi.log import HeaderLogger
from wsgidav.dav_error import HTTP_FORBIDDEN, DAVError
from wsgidav.dav_provider import DAVNonCollection
from wsgidav.dir_browser import WsgiDavDirBrowser
from wsgidav.error_printer import ErrorPrinter
from wsgidav.mw.debug_filter import WsgiDavDebugFilter
from wsgidav.request_resolver import RequestResolver

from alexandria.core.models import File


class MyBytesIO(io.BytesIO):
    """
    Custom BytesIO.

    We're writing the DAV-file into a `BytesIO`, so we can perform the actual saving in
    `AlexandriaFileResource.end_write()`. This is needed, to make sure the file is
    scanned for viruses and encrypted in storage, if one of those features is enabled.
    `wsgidav.RequestServer.do_PUT` would close the file after writing, thus making its
    content unavailable in `AlexandriaFileResource.end_write()`. This class just
    overrides the `close()`-method in order to prevent closing. Afterward, we have to
    manually call `.do_close()` to clean up.
    """

    def close(self):
        # prevent closing the file
        return

    def do_close(self):
        return super().close()


class AlexandriaFileResource(ManabiFileResourceMixin, DAVNonCollection):
    def __init__(
        self,
        path,
        environ,
        *,
        cb_hook_config=None,
    ):
        self.provider: AlexandriaProvider
        super().__init__(path, environ)
        self._cb_config = cb_hook_config
        self._token = environ["manabi.token"]
        self.user, self.group, file_pk = self._token.payload

        # We only serve the newest original File of the Document.
        self.file = (
            File.objects.get(pk=file_pk)
            .document.files.filter(variant=File.Variant.ORIGINAL)
            .order_by("-created_at")
            .first()
        )
        self.memory_file = MyBytesIO()
        self.name = Path(self.path).name

    def _get_timestamp(self, dt):
        return time.mktime(dt.timetuple())

    def support_etag(self):
        # we only support etag with S3Storage
        if hasattr(self.file.content.file, "obj"):
            return True

    def get_content_length(self):
        return self.file.content.size

    def get_content_type(self):
        return self.file.mime_type

    def get_creation_date(self):
        return self._get_timestamp(self.file.created_at)

    def get_etag(self):
        if self.support_etag():
            return self.file.content.file.obj.e_tag.strip('"')

    def get_last_modified(self):
        return self._get_timestamp(self.file.modified_at)

    def get_content(self):
        assert not self.is_collection
        return self.file.content.file

    def begin_write(self, *, content_type=None):
        self.process_pre_write_hooks()
        assert not self.is_collection
        if self.provider.readonly:  # pragma: no cover
            raise DAVError(HTTP_FORBIDDEN)
        return self.memory_file

    def end_write(self, *, with_errors):
        try:
            validate_file_infection(self.memory_file)
        except ValidationError:
            raise DAVError(HTTP_FORBIDDEN)

        file = self.file
        if (
            self.file.modified_by_user != self.user
            or self.file.modified_by_group != self.group
        ):
            file = File(
                variant=self.file.variant,
                original=self.file.original,
                name=self.file.name,
                document=self.file.document,
                encryption_status=self.file.encryption_status,
                mime_type=self.file.mime_type,
                modified_by_user=self.user,
                modified_by_group=self.group,
            )
        file.size = self.memory_file.getbuffer().nbytes
        self.memory_file.seek(0)
        django_file = DjangoFile(name=file.name, file=self.memory_file)
        file.content = django_file
        file.save()
        self.file = file
        self.memory_file.do_close()
        super().end_write(with_errors=with_errors)


class AlexandriaProvider(ManabiProvider):
    def get_file_resource(self, path, environ, _):
        try:
            return AlexandriaFileResource(
                path,
                environ,
                cb_hook_config=self._cb_hook_config,
            )
        except File.DoesNotExist:
            return None


def get_dav():
    postgres_dsn = (
        f"dbname={settings.DATABASES['default']['NAME']} "
        f"user={settings.DATABASES['default']['USER']} "
        f"host={settings.DATABASES['default']['HOST']} "
        f"password={settings.DATABASES['default']['PASSWORD']}"
    )
    ttl = 600
    root_folder = settings.MEDIA_ROOT
    if settings.ALEXANDRIA_FILE_STORAGE == "alexandria.storages.backends.s3.S3Storage":
        root_folder = "/"

    config = {
        "lock_storage": ManabiDbLockStorage(ttl, postgres_dsn),
        "provider_mapping": {
            settings.ALEXANDRIA_MANABI_DAV_URL_PATH: AlexandriaProvider(
                root_folder, cb_hook_config=None
            ),
        },
        "middleware_stack": [
            HeaderLogger,
            WsgiDavDebugFilter,
            ErrorPrinter,
            ManabiAuthenticator,
            WsgiDavDirBrowser,
            RequestResolver,
        ],
        "manabi": {
            "key": settings.MANABI_SHARED_KEY,
            "refresh": ttl,
            "initial": ttl,
            "secure": settings.MANABI_SECURE,
        },
    }
    return ManabiDAVApp(config)
