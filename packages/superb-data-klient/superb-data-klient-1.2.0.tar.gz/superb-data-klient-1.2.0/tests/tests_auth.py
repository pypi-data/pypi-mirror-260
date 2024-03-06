import unittest
import webbrowser
import superbdataklient as sdk


class AuthenticationTestSDKClient(unittest.TestCase):
    env = 'sdk-dev'

    def test_get_organization_all(self):
        """
        instantiating a SDKClient should raise EnvironmentError in a no-browser-environment
        """
        try:
            webbrowser.get()
            sdk.SDKClient(env=self.env)
        except webbrowser.Error:
            with self.assertRaises(EnvironmentError):
                sdk.SDKClient(env=self.env)


if __name__ == '__main__':
    unittest.main()
