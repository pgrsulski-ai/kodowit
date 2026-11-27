import unittest, base64
from check_deployment import check
class Deployment(unittest.TestCase):
    def config(self,url='',key=''): return f"globalThis.KODOWIT_CLOUD_CONFIG = {{url:'{url}', key:'{key}'}};"
    def test_offline(self): self.assertIn('offline',check(self.config()))
    def test_production_empty(self):
        with self.assertRaises(ValueError): check(self.config(),True)
    def test_public(self): self.assertIn('niezweryfikowany',check(self.config('https://abc.supabase.co','sb_publishable_test'),True))
    def test_secret(self):
        for key in ['sb_secret_test','x.'+base64.urlsafe_b64encode(b'{"role":"service_role"}').decode()+'.x']:
            with self.assertRaises(ValueError): check(self.config('https://abc.supabase.co',key))
    def test_bad_url(self):
        with self.assertRaises(ValueError): check(self.config('https://example.com','sb_publishable_test'))
if __name__=='__main__': unittest.main()
