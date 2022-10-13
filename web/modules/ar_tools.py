import io
import requests as r


def download_model(gbl_url):
    """Download gbl model to a variable"""
    print(gbl_url, 'Try')
    with r.get(gbl_url, stream=True) as resp:
        resp.raise_for_status()
        with io.BytesIO() as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
            return f


if __name__ == '__main__':
    f = download_model('https://github.com/maxfyk/maxfyk.github.io/raw/master/assets/phoenix.glb')
    print(f)