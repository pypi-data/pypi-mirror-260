import os
import logging
from io import BytesIO
from typing import Dict, Union
from file_system.file import File
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pydrive.auth import ServiceAccountCredentials
from oauth2client.clientsecrets import InvalidClientSecretsError
from pydrive.settings import InvalidConfigError


class GDrive:

    def __init__(
        self,
        folder_id: Union[str, None] = None,
        download_path: Union[str, None] = None,
        client_secrets_file: Union[str, None] = None
    ) -> None:
        self.log = logging.getLogger("GDrive")
        self.folder_id = folder_id or os.getenv("FOLDER_ID")
        self.download_path = download_path or os.getenv(
            "DOWNLOAD_PATH",
            "./downloads"
        )
        self.cs_file = client_secrets_file or os.getenv(
            "CLIENT_SECRETS_FILE",
            "./client_secrets.json"
        )
        self.drive = self.authorize()

    def authorize(self) -> GoogleDrive:
        gauth = GoogleAuth()
        gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(
            self.cs_file, ['https://www.googleapis.com/auth/drive']
        )
        gauth.Authorize()
        drive = GoogleDrive(gauth)
        self.log.info("Google Drive yetkilendirme yapıldı.")
        return drive

    def path_clear(self, path: str) -> str:
        # eğer son karakter "/" ise kaldırılır
        if path.endswith("/"):
            path = path[:-1]

        # eğer başlangıçta "./" varsa kaldırılır
        if path.startswith("./"):
            path = path[2:]

        # eğer başlangıçta "/" varsa kaldırılır
        if path.startswith("/"):
            path = path[1:]

        return path

    def _create_file(self, meta_data: Dict, file_path: Union[str, None] = None):
        # Görseli Google Drive'a yükle
        file = self.drive.CreateFile(meta_data)
        if file_path:
            file.SetContentFile(file_path)
        file.Upload()

        return file

    def create_folders(self, path: str) -> str:
        """Tek bir klasör veya klasör ağaç yapısı oluşturur

        Args:
            path (str): Klasör yolu

        Returns:
            str: Google drive son klasör id'si
        """
        path = self.path_clear(path)
        folder_names = path.split('/')
        folder_id = self.folder_id

        for folder_name in folder_names:
            folder_id = self.create_folder(folder_id, folder_name)

        return folder_id

    def create_folder(self, folder_id, folder_name):
        metadata = {
            "title": folder_name,
            "parents": [{'id': folder_id}],
            "mimeType": "application/vnd.google-apps.folder"
        }
        folder = self._create_file(metadata)

        return folder["id"]

    def upload_image(self, image_path: str, folder_id: Union[str, None] = None):
        filename = File.get_filename(image_path)

        # klasör yapısını oluştur
        folder_id = folder_id or self.folder_id

        # Yüklenecek görselin dosya yolu
        file_metadata = {
            'title': filename,  # Görselin dosya adı
            # Görseli yüklemek istediğiniz klasörün ID'si
            'parents': [{'id': folder_id}]
        }

        # Görseli Google Drive'a yükle
        try:
            file = self._create_file(file_metadata, image_path)
            self.log.info(f"Görsel Google Drive'a yüklendi: {image_path}")
        except (InvalidClientSecretsError, InvalidConfigError) as e:
            self.log.error(f"Yükleme esnasında bir hata oldu: {str(e)}")
            self.drive = self.authorize()
            self.upload_image(image_path)

        return file['id']

    def download_image(self, file_id, output_path: str = None) -> BytesIO:
        if not output_path:
            output_path = self.download_path

        # klasör yoksa oluşturulur
        File.create_directory(output_path)
        filename = f"{output_path}/{file_id}.png"

        # Dosya daha önce indirildi ise onu gönder
        if File.exists(filename):
            return filename

        # Dosya ID'sini kullanarak dosyayı indirme
        file = self.drive.CreateFile({'id': file_id})
        file.GetContentFile(filename=filename)
        return file.content  # BytesIO
