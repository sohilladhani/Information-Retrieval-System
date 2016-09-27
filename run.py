#!/usr/bin/python
"""This module runs other modules in the software"""
def main_run():
    """This method runs the other modules by first checking if it is the first run of the software on the sytem. \nIf so it builds necessary indexes first and then proceed to take queries from the user"""
    first_run = open('first_run.indicator', 'rb').read()
    first_run = int(first_run)
    if first_run != 0:
        print "Attempting first run. This may take few seconds..."
        import indexer
        import normalize
        open('first_run.indicator', 'wb').write('0')
    import query

main_run()

