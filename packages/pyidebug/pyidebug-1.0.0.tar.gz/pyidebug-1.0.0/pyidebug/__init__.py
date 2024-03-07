'''
PyIDebug

Module that allows you to interactively debug your code.
'''

__all__ = ["debug", "showInfo"]
__version__ = "1.0.0"
__author__ = "Natanael Quintino"
__email__ = "natanael.quintino@ipiaget.pt"

def debug(globals, locals=None, title=None):
    """Interactive debug that allow you change and create variables dynamically"""
    if title is not None:
        # Report debug zone begin
        showInfo(f'{title.title()} interaction zone begin')

    while True:
        try:
            code = input('\nType your test code: ')

            if code.lower() in ['q', 'exit']:
                raise KeyboardInterrupt

            if any(code):
                if '=' in code and '==' not in code:
                    exec(code, globals, locals)
                elif code.isalpha():
                    value = eval(code, globals, locals)
                    print('\n\t', f'{code} = {value}',
                          end='\n')
                else:
                    print('\n\t', eval(code, globals, locals), end='\n')
            else:
                print('\n\n*** Nothing typed *** Press CTRL+C to skip ***\n')

        except (KeyboardInterrupt, EOFError):
            # Break a line
            print()

            # Stop the loop
            break

        except Exception as err:
            # Show the error
            print(f'\n{err.__class__.__name__}: {err}\n')

    if title is not None:
        # Report debug zone end
        showInfo(f'{title.title()} interaction zone end')

    return None


def showInfo(info: str) -> (None):
    """Show the info with delimiters in screen"""
    delimiter = len(message)*"="
    print(delimiter, message, delimiter, sep='\n')
    return None
