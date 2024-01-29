import unittest
from server.src.utility.password_utility import generate_hash, check_password


class TestPasswordUtility(unittest.TestCase):
    def test_generate_hash(self):
        password = "test_password"
        generated_hash = generate_hash(password)

        # Check that a hash is generated
        assert generated_hash is not None
        # Check that the hash is not the same as the plaintext password
        assert generated_hash != password

    def test_check_password(self):
        password = "test_password"
        wrong_password = "wrong_password"
        generated_hash = generate_hash(password)

        # Check that the correct password returns True
        assert check_password(password, generated_hash)
        # Check that the incorrect password returns False
        assert not check_password(wrong_password, generated_hash)

    # This test will check if the hash is consistent
    def test_generate_hash_consistency(self):
        password = "consistent_password"
        hash1 = generate_hash(password)
        hash2 = generate_hash(password)

        # The same password should generate different hashes due to the salt
        assert hash1 != hash2
        # But both should be valid for the original password
        assert check_password(password, hash1)
        assert check_password(password, hash2)


if __name__ == '__main__':
    unittest.main()
