"""
SkylabStudio - Python Client
For more information, visit https://studio.skylabtech.ai
"""

import asyncio
import aiohttp
import json
import logging
import pyvips
import os
import time
import hmac
import base64
import hashlib
import requests
from io import BytesIO

from .version import VERSION
from .studio_exception import StudioException

API_HEADER_KEY = 'X-SLT-API-KEY'
API_HEADER_CLIENT = 'X-SLT-API-CLIENT'

LOGGER = logging.getLogger('skylab_studio')
LOGGER.propagate = False

class api: #pylint: disable=invalid-name
    """
    The client for accessing the Skylab Studio platform.

    Args:c   
        api_key (str): Your account's API KEY.

    Attributes:
        api_version (str): The API endpoint version number.
        api_key (str): The API key to use.
        debug (boolean): Whether or not to allow debugging information to be printed.
    """

    # initialization
    try:
        api_url = os.environ['SKYLAB_API_URL']
    except KeyError:
        api_url = 'https://studio.skylabtech.ai:443'

    # this is not package version -> used to construct the request base url
    api_version = '1'
    api_key = 'THIS_IS_A_TEST_API_KEY'

    debug = False

    def __init__(self, api_key=None, **kwargs):
        if not api_key:
            raise Exception("You must specify an api key")

        self.api_key = api_key
        self.max_concurrent_downloads = 5

        if 'api_version' in kwargs:
          self.api_version = kwargs['api_version']

        if 'debug' in kwargs:
            self.debug = kwargs['debug']
        
        if 'max_concurrent_downloads' in kwargs:
            self.max_concurrent_downloads = kwargs['max_concurrent_downloads']

        if self.debug:
            logging.basicConfig(format='%(asctime)-15s %(message)s', level=logging.DEBUG)

            LOGGER.debug('Debug enabled')
            LOGGER.propagate = True

    def _build_http_auth(self):
        return (self.api_key, '')

    def _build_request_headers(self):
        client_header = '%s-%s' % (
            'python',
            VERSION
        )

        headers = {
            API_HEADER_CLIENT: client_header,
            'X-SLT-API-KEY': self.api_key,
            'Content-type': 'application/json',
            'Accept': 'text/plain'
        }

        return headers

    def _build_request_path(self, endpoint):
        path = '/api/public/v%s/%s' % (self.api_version, endpoint)

        path = "%s%s" % (
            self.api_url,
            path
        )

        return path

    @staticmethod
    def _build_payload(data):
        if not data:
            return None

        return json.dumps(data)

    def _api_request(self, endpoint, http_method, **kwargs):
        """Private method for api requests"""
        LOGGER.debug(' > Sending API request to endpoint: %s', endpoint)

        headers = self._build_request_headers()
        LOGGER.debug('\theaders: %s', headers)

        path = self._build_request_path(endpoint)
        LOGGER.debug('\tpath: %s', path)

        data = self._build_payload(kwargs.get('payload'))
        if not data:
            data = kwargs.get('data')
        LOGGER.debug('\tdata: %s', data)

        req_kw = dict(
            headers=headers,
        )

        try:
          if http_method == 'POST':
              if data:
                  response = requests.post(path, data=data, **req_kw)
              else:
                  response = requests.post(path, **req_kw)
          elif http_method == 'PUT':
              response = requests.put(path, data=data, **req_kw)
          elif http_method == 'DELETE':
              response = requests.delete(path, **req_kw)
          else:
              response = requests.get(path, data=data, **req_kw)

          LOGGER.debug('\tresponse code:%s', response.status_code)

          try:
              LOGGER.debug('\tresponse: %s', response.json())
          except ValueError:
              LOGGER.debug('\tresponse: %s', response.content)

          if not response.ok:
              status_code = response.status_code
              message = response.json()['message']

              raise StudioException(status_code, message)
        except (StudioException, Exception) as e:
              formatted_response = {
                  "message": e.message,
                  "status": e.status_code
              }
              return formatted_response

        return response.json()
    
    ###### JOB ENDPOINTS ######

    def list_jobs(self):
        """ API call to get all jobs """
        return self._api_request(
            'jobs',
            'GET'
        )

    def create_job(self, payload=None):
        """ API call to create a job """
        return self._api_request(
            'jobs',
            'POST',
            payload=payload
        )

    def get_job(self, job_id):
        """ API call to get a specific job """
        return self._api_request(
            'jobs/%s' % job_id,
            'GET'
        )

    def get_job_by_name(self, payload=None):
        return self._api_request(
            'jobs/find_by_name',
            'GET',
            payload=payload
        )

    def update_job(self, job_id, payload=None):
        """ API call to update a specific job """
        return self._api_request(
            'jobs/%s' % job_id,
            'PATCH',
            payload=payload
        )

    def queue_job(self, job_id, payload=None):
        return self._api_request(
            'jobs/%s/queue' % job_id,
            'POST',
            payload=payload
        )

    def fetch_jobs_in_front(self, job_id):
        return self._api_request(
            'jobs/%s/jobs_in_front' % job_id,
            'GET',
        )

    def delete_job(self, job_id):
        """ API call to delete a specific job """
        return self._api_request(
            'jobs/%s' % job_id,
            'DELETE'
        )

    def cancel_job(self, job_id):
        """ API call to cancel a specific job """
        return self._api_request(
            'jobs/%s/cancel' % job_id,
            'POST'
        )
    
    ###### PROFILE ENDPOINTS ######

    def list_profiles(self):
        """ API call to get all profiles """
        return self._api_request(
            'profiles',
            'GET'
        )

    def create_profile(self, payload=None):
        """ API call to create a profile """
        return self._api_request(
            'profiles',
            'POST',
            payload=payload
        )

    def get_profile(self, profile_id):
        """ API call to get a specific profile """
        return self._api_request(
            'profiles/%s' % profile_id,
            'GET'
        )

    def update_profile(self, profile_id, payload=None):
        """ API call to update a specific profile """
        return self._api_request(
            'profiles/%s' % profile_id,
            'PATCH',
            payload=payload
        )

    ###### PHOTO ENDPOINTS ######

    def _get_upload_url(self, payload={"use_cache_upload": False}):
      return self._api_request('photos/upload_url', 'GET', payload=payload)

    # todo privatize this method and test photo_upload
    def _create_photo(self, payload=None):
        """ API call to create a photo """
        return self._api_request(
            'photos',
            'POST',
            payload=payload
        )

    def calculate_md5(self, file_path):
        md5_hash = hashlib.md5()
        with open(file_path, "rb") as file:
            for chunk in iter(lambda: file.read(4096), b""):
                md5_hash.update(chunk)
        return md5_hash.hexdigest()
    
    def upload_job_photo(self, photo_path, id):
        return self._upload_photo(photo_path, id, 'job')

    def upload_profile_photo(self, photo_path, id):
        return self._upload_photo(photo_path, id, 'profile')

    def _upload_photo(self, photo_path, id, model='job'):
        res = {}
        valid_exts_to_check = ('.jpg', '.jpeg', '.png', '.webp')
        if not photo_path.lower().endswith(valid_exts_to_check):
            raise Exception('Invalid file type: must be of type jpg/jpeg/png/webp')

        file_size = os.path.getsize(photo_path)
        if file_size > 27 * 1024 * 1024:
            raise Exception('Invalid file size: must be no larger than 27MB')

        photo_name = os.path.basename(photo_path)
        headers = {}

        # Read file contents to binary
        with open(photo_path, "rb") as file:
            data = file.read()
            md5hash = hashlib.md5(data).hexdigest()

        # model - either job or profile (job_id/profile_id)
        photo_data = { f"{model}_id": id, "name": photo_name, "use_cache_upload": False }

        if model == 'job':
            job_type = self.get_job(id)['type']

            if job_type == 'regular':
                headers = { 'X-Amz-Tagging': 'job=photo&api=true' }

        # Ask studio to create the photo record
        photo_resp = self._create_photo(photo_data)
        if not photo_resp:
            raise Exception('Unable to create the photo object, if creating profile photo, ensure enable_extract and replace_background is set to: True')

        photo_id = photo_resp['id']
        res['photo'] = photo_resp

        # md5 = self.calculate_md5(photo_path)
        b64md5 = base64.b64encode(bytes.fromhex(md5hash)).decode('utf-8')
        payload = {
            "use_cache_upload": False,
            "photo_id": photo_id,
            "content_md5": b64md5
        }

        # Ask studio for a presigned url
        upload_url_resp = self._get_upload_url(payload=payload)
        upload_url = upload_url_resp['url']

        # PUT request to presigned url with image data
        headers["Content-MD5"] = b64md5

        try:
          upload_photo_resp = requests.put(upload_url, data, headers=headers)

          if not upload_photo_resp:
            print('First upload attempt failed, retrying...')
            retry = 0
            # retry upload
            while retry < 3:
                upload_photo_resp = requests.put(upload_url, data, headers=headers)

                if upload_photo_resp:
                    break  # Upload was successful, exit the loop
                elif retry == 2:  # Check if retry count is 2 (0-based indexing)
                    raise Exception('Unable to upload to the bucket after retrying.')
                else:
                    time.sleep(1)  # Wait for a moment before retrying
                    retry += 1

        except Exception as e:
          print(f"An exception of type {type(e).__name__} occurred: {e}")
          print('Deleting created, but unuploaded photo...')
          self.delete_photo(photo_id)

        res['upload_response'] = upload_photo_resp.status_code
        return res

    def get_photo(self, photo_id):
        """ API call to get a specific photo """
        return self._api_request(
            'photos/%s' % photo_id,
            'GET'
        )

    def get_job_photos(self, job_identifier, value):
        """
          job identifier - either id or name
          value - the actual job_id or job_name
        """
        payload = {
            f"job_{job_identifier}": value
        }
        return self._api_request(
            'photos/list_for_job',
            'GET',
            payload=payload
        )

    def delete_photo(self, photo_id):
        """ API call to delete a specific photo """
        return self._api_request(
            'photos/%s' % photo_id,
            'DELETE'
        )

    def validate_hmac_headers(self, secret_key, job_json, request_timestamp, signature):
        message=f"{request_timestamp}:{job_json}".encode('utf-8')

        # Create the HMAC signature using SHA-256
        hmac_digest = hmac.new(secret_key.encode('utf-8'), message, hashlib.sha256).digest()
        generated_sig = base64.b64encode(hmac_digest).decode('utf-8')

        # Compare rails to python signature
        return signature == generated_sig
    
    ###### DOWNLOAD HELPERS ######

    async def _download_bg_images(self, profile):
        temp_bgs = []
        bg_photos = [photo for photo in profile["photos"] if photo["jobId"] == None]

        for bg in bg_photos:
            bg_buffer = await self._download_image(bg["originalUrl"])
            bg_image = pyvips.Image.new_from_buffer(bg_buffer, "")
            temp_bgs.append(bg_image)

        return temp_bgs if temp_bgs else None
    
    async def _download_image(self, image_url):
        if not image_url.lower().startswith("http"):
            raise Exception(f'Invalid retouchedUrl: "{image_url}" - Please ensure the job is complete')

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url) as response:
                    image_buffer = await response.read()
                    return image_buffer
        except aiohttp.ClientError as ex:
            print(f'Error downloading image: {ex}')
            return None
    
    async def _download_replaced_bg_image(self, file_name, input_image, output_path, profile = None, bgs = None):
        try:
            output_file_type = profile["outputFileType"] if profile else "png"

            if bgs is None and profile and profile.get("photos"):
                bgs = await self._download_bg_images(profile)

            alpha_channel = input_image[3]
            rgb_channel = input_image[0:3]
            rgb_cutout = rgb_channel.bandjoin(alpha_channel)

            if bgs and len(bgs) > 0:
                for i, bg_image in enumerate(bgs):
                    new_file_name = f"{os.path.splitext(file_name)[0]} ({i + 1}).{output_file_type}" if i > 0 else f"{os.path.splitext(file_name)[0]}.{output_file_type}"
                    resized_bg_image = bg_image.thumbnail_image(input_image.width, height=input_image.height, crop=pyvips.Interesting.CENTRE)
                    result_image = resized_bg_image.composite2(rgb_cutout, pyvips.BlendMode.OVER)
                    result_image.write_to_file(os.path.join(output_path, new_file_name))

            return True
        except Exception as ex:
            print(f"Error downloading background image: {ex}")
            return False

    async def download_all_photos(self, photos_list, profile, output_path):
        if not os.path.exists(output_path):
            raise Exception("Invalid output path")
        
        success_photos = []
        errored_photos = []
        bgs = []

        try:
            # Ensure the profile has photos and download background images
            profile = self.get_profile(profile['id'])
            if profile['photos']:
                bgs = await self._download_bg_images(profile)
            
            photo_ids = [photo["id"] for photo in photos_list]
            photo_options = {
                'bgs': bgs
            }
            download_tasks = []
            semaphore = asyncio.Semaphore(self.max_concurrent_downloads)

            for photo_id in photo_ids:
                download_tasks.append(self.download_photo(photo_id, output_path, profile, photo_options, semaphore))

            # Wait for all download tasks to complete
            results = await asyncio.gather(*download_tasks)
            for result in results:
                if result[1]:
                    success_photos.append(result[0])
                else:
                    errored_photos.append(result[0])

            return { 'success_photos': success_photos, 'errored_photos': errored_photos }

        except Exception as e:
            print(e)

            return { 'success_photos': success_photos, 'errored_photos': errored_photos }
    
    async def download_photo(self, photo_id, output_path, profile = None, options = {}, semaphore = None):
        if not os.path.exists(output_path):
            raise Exception("Invalid output path")
        elif semaphore != None:
            await semaphore.acquire()

        photo = self.get_photo(photo_id)
        profile_id = photo['job']['profileId']
        file_name = photo['name']
        
        try:
            if profile is None:
                profile = self.get_profile(profile_id)

            is_extract = bool(profile.get('enableExtract', False))
            replace_background = bool(profile.get('replaceBackground', False))
            is_dual_file_output = bool(profile.get('dualFileOutput', False))
            enable_strip_png_metadata = bool(profile.get('enableStripPngMetadata', False))
            bgs = options.get('bgs') if options else None

            # Load output image
            image_buffer = await self._download_image(photo['retouchedUrl'])
            image = pyvips.Image.new_from_buffer(image_buffer, "")

            if is_extract:  # Output extract image
                png_file_name = f"{os.path.splitext(file_name)[0]}.png"

                # Dual File Output will provide an image in the format specified in the outputFileType field
                # and an extracted image as a PNG.
                if is_dual_file_output:
                    image.write_to_file(os.path.join(output_path, png_file_name))

                if replace_background:
                    await self._download_replaced_bg_image(file_name, image, output_path, profile, bgs)

                # Regular Extract output
                if not is_dual_file_output and not replace_background:
                    image.write_to_file(os.path.join(output_path, png_file_name))
            else:  # Non-extracted regular image output
                image.write_to_file(os.path.join(output_path, file_name))

            print(f"Successfully downloaded: {file_name}")
            return file_name, True
        except Exception as e:
            print(f"Failed to download photo id: {photo_id}")
            print(e)
            return file_name, False
        finally:
            if semaphore != None:
                semaphore.release()
    