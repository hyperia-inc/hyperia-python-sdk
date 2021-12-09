
if __name__ == '__main__':
    """
    Writes the API key to api_key.txt file. It will create the file if it doesn't exist.
    This function is intended to be called from the Python command line using: python hyperia YOUR_API_KEY
    If you don't have an API key yet, register for one at: https://hyperia.net/api/register

    INPUT:
    argv[1] -> Your API key from Hyperia. Should be 73 hex characters

    OUTPUT:
    none
    """

    import sys
    if len(sys.argv) == 2 and sys.argv[1]:
        if len(sys.argv[1]) == 73:
            # write the key to the file
            f = open('api_key.txt', 'w')
            f.write(sys.argv[1])
            f.close()
            print('Key: ' + sys.argv[1] + ' was written to api_key.txt')
            print(
                'You are now ready to start using Hyperia. For an example, run: python example.py')
        else:
            print(
                'The key appears to invalid. Please make sure to use the 73 character key assigned by Hyperia')
    else:
        print(
            'The key appears to invalid. Please make sure to use the 73 character key assigned by Hyperia')


