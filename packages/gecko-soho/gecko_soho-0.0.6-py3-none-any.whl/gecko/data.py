import datetime
import os
import logging
import re
import requests
from typing import List

from PIL import Image


logger = logging.getLogger()


class DataLoader:

    def __init__(self, base_url: str, data_dir='./data/soho/tmp') -> None:
        self.base_url = base_url
        self.data_dir = os.path.abspath(data_dir)
        os.makedirs(self.data_dir, exist_ok=True)

    def get_daterange(self, start_date, end_date):
        for n in range(int((end_date - start_date).days) + 1):
            yield start_date + datetime.timedelta(n)

    def get_image_by_path(self, img_path: str) -> Image:
        return Image.open(img_path)

    def download_single(self, url: str, output_path: str, download_format: str) -> None:
        try:
            resp = requests.get(
                url=url,
                params={'downloadformat': download_format}
            )
            if resp.ok is True:
                with open(output_path, mode='wb') as f:
                    f.write(resp.content)
        except Exception as e:
            logger.error(f'Failed to load single URL: {url}')
            raise(e)


class JPEGDataLoader(DataLoader):

    def __init__(self, camera: str, data_dir: str='./data/soho/jpeg') -> None:
        self._year_escape_str = '<<<YEAR>>>'
        self.camera = camera
        if camera not in ('c2', 'c3'):
            raise ValueError(f'`camera` parameter should be one of these: c2, c3. You\'ve passed {camera}')

        super().__init__(
            base_url=f'https://soho.nascom.nasa.gov/data/REPROCESSING/Completed/{self._year_escape_str}/{camera}/',
            data_dir=data_dir
        )

    def ls_images(self, start_datetime: datetime.datetime, end_datetime: datetime.datetime):
        # list all SOHO image basenames existing
        res = []
        imgs = []
        for _date in self.get_daterange(start_datetime.date(), end_datetime.date()):
            imgs += self.ls_images_per_date(_date)

        for img in imgs:
            img_dt = datetime.datetime.strptime(img[:13], '%Y%m%d_%H%M')
            if img_dt < end_datetime and img_dt > start_datetime:
                res.append(img)
        
        return res

    def ls_images_per_date(self, img_date: datetime.date) -> List[str]:
        date_str = datetime.datetime.strftime(img_date, '%Y%m%d')
        base_url = self.base_url.replace(self._year_escape_str, str(img_date.year))
        ls_url = os.path.join(base_url, date_str)
        logger.info(f'Listing images from: {ls_url}')
        resp = requests.get(ls_url)
        
        if resp.ok is False:
            raise RuntimeError(f'Failed to fetch data from {ls_url}: {resp.content.decode()}')

        return sorted(list(set(re.findall(r'\d+_\d+_c\d_1024.jpg', resp.content.decode()))))
    
    def construct_url(self, img_name: str) -> str:
        base_url = self.base_url.replace(self._year_escape_str, img_name[:4])
        return os.path.join(base_url, img_name[:8], img_name)

    def construct_local_path(self, img_name: str) -> str:
        return os.path.join(self.data_dir, self.camera, img_name[:8], img_name)

    def check_is_downloaded(self, img_name: str) -> bool:
        return os.path.exists(self.construct_local_path(img_name))

    def get_image(self, img_name) -> Image:
        # image name is a basename like `20230723_0000_c2_1024.jpg``
        # if doesn't persist local - download it
        d_url = self.construct_url(img_name)
        d_output = self.construct_local_path(img_name)
        if self.check_is_downloaded(img_name) is False:
            os.makedirs(os.path.join(self.data_dir, self.camera, img_name[:8]), exist_ok=True)
            self.download_single(url=d_url, output_path=d_output, download_format='jpg')
        return self.get_image_by_path(d_output)

    def download_full_date(self, download_date: datetime.date) -> None:
        date_str = datetime.datetime.strftime(download_date, '%Y%m%d')
        base_url = self.base_url.replace(self._year_escape_str, str(download_date.year))
        all_images = self.ls_images_per_date(download_date)

        for img in all_images:
            d_url = os.path.join(base_url, date_str, img)
            output_dir = os.path.join(self.data_dir, self.camera, date_str)
            os.makedirs(output_dir, exist_ok=True)
            d_output = os.path.join(output_dir, img)
            if not os.path.exists(d_output):
                logger.info(f'Downloading {d_url} to {d_output}')
                self.download_single(d_url, d_output, 'jpg')
