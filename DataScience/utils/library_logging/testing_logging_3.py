# myapp.py
import logging
import testing_logging_4

def main():
    logging.basicConfig(filename='./myapp.log', level=logging.INFO)
    logging.info('Started')
    testing_logging_4.do_something()
    logging.info('Finished')

if __name__ == '__main__':
    main() 