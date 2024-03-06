class AdvancedPrinter:
    """
    Custom class to mimic the behavior of the print function with added color and style options.

    - For more colors call the 'help' method

    Colors for text and background:
        - BLACK
        - WHITE
        - RED
        - GREEN
        - YELLOW
        - BLUE
        - MAGENTA
        - CYAN
        - ORANGE
        - GRAY
        - OLIVE

    Text styles:
        - B (Bold)
        - IT (Italic)
        - U (Underline)
        - INV (Invert)
        - STR (Strike-through)
    """

    class C:
        """
        Nested class containing ANSI escape codes for different text colors and styles.
        """
        RESET = '\033[0m'

        BLACK = '\033[30m'
        WHITE = '\033[97m'

        RED = '\033[31m'
        RED1 = '\033[91m'
        RED2 = '\033[38;2;128;0;0m'

        GREEN = '\033[38;2;0;128;0m'
        GREEN1 = '\033[32m'
        GREEN2 = '\033[92m'
        GREEN3 = '\033[38;2;0;255;0m'

        YELLOW = '\033[33m'
        YELLOW1 = '\033[93m'
        YELLOW2 = '\033[38;2;255;255;0m'

        OLIVE = '\033[38;2;128;128;0m'

        BLUE = '\033[34m'
        BLUE1 = '\033[94m'
        BLUE2 = '\033[38;2;0;0;255m'
        BLUE3 = '\033[38;2;0;0;128m'

        MAGENTA = '\033[35m'
        MAGENTA1 = '\033[38;2;255;0;255m'

        PINK = '\033[95m'

        PURPLE = '\033[38;2;128;0;128m'

        CYAN = '\033[38;2;0;128;128m'
        CYAN1 = '\033[36m'
        CYAN2 = '\033[96m'

        ORANGE = '\033[38;5;208m'

        GRAY = '\033[90m'
        GRAY1 = '\033[37m'

        # Background Colors
        BG_BLACK = '\033[40m'
        BG_WHITE = '\033[107m'

        BG_GRAY = '\033[47m'
        BG_GRAY1 = '\033[100m'

        BG_RED = '\033[41m'
        BG_RED1 = '\033[101m'

        BG_GREEN = '\033[42m'
        BG_GREEN1 = '\033[102m'

        BG_YELLOW = '\033[103m'
        BG_OLIVE = '\033[43m'

        BG_BLUE = '\033[44m'
        BG_BLUE1 = '\033[104m'

        BG_MAGENTA = '\033[45m'

        BG_PINK = '\033[105m'

        BG_CYAN = '\033[46m'
        BG_CYAN1 = '\033[106m'

        BG_ORANGE = '\033[48;5;208m'
        BG_ORANGE1 = '\033[48;5;202m'
        BG_BROWN = '\033[48;5;166m'

        # Styles
        B = '\033[1m'
        IT = '\x1B[3m'
        U = '\x1B[4m'
        INV = '\u001b[7m'
        STR = '\u001b[9m'

    @staticmethod
    def _prepare_text(*args, foreground=None, background=None, style=None):
        """
        Helper method to prepare the colored and styled text.

        :param args: The text to print.
        :param foreground: The text color.
        :param background: The background color.
        :param style: The style.
        :return: The colored and styled text.
        """
        color_code = getattr(AdvancedPrinter.C, foreground.upper(), '') if foreground else ''
        background_code = getattr(AdvancedPrinter.C, f"BG_{background.upper()}", '') if background else ''

        # Process s
        style_code = ''
        if style:
            styles = style.split('-')
            for style in styles:
                style_code += getattr(AdvancedPrinter.C, style.upper(), '')

        text = ' '.join(str(arg) for arg in args)
        return f'{background_code}{style_code}{color_code}{text}{AdvancedPrinter.C.RESET}'

    @staticmethod
    def print(*args, c=None, b=None, s=None, end='\n', flush=False, file=None, **kwargs):
        """
        Print function wrapper with added color and style options.

        :param args: The text to print.
        :param c: The text color
        :param b: The background color.
        :param s: The style.
        :param end: The string appended after the last value, default is a newline.
        :param flush: Whether to forcibly flush the stream, default is False.
        :param file: A file-like object (stream); defaults to the current sys.stdout.
        :param kwargs: Additional keyword arguments supported by the built-in print function.
        """
        colored_text = AdvancedPrinter._prepare_text(*args, foreground=c, background=b, style=s)
        print(colored_text, end=end, flush=flush, file=file, **kwargs)

    @staticmethod
    def line(*args, c=None, b=None, s=None, end='') -> str:
        """
        Custom function with added color and style options used for inline printing

        :param args: The text to return.
        :param c: The text color.
        :param b: The background color.
        :param s: The style.
        :param end: The string appended after the last value, default is ''.
        """
        colored_text = AdvancedPrinter._prepare_text(*args, foreground=c, background=b, style=s)
        return f"{colored_text}{end}"

    @staticmethod
    def input(*args, c=None, b=None, s=None):
        """
        Input function wrapper with added color and style options

        :param args: The text to print.
        :param c: The text color
        :param b: The background color.
        :param s: The style.
        :return: Return the inbuilt 'input' function but with colored formatting
        """
        text = args[0]
        formatted_text = AdvancedPrinter._prepare_text(text.strip(), foreground=c, background=b, style=s)
        return input(formatted_text + ' ') if text.endswith(' ') else input(formatted_text)

    @staticmethod
    def frame(text, f_s='basic', f_c=None, f_b=None, c=None, b=None, s=None):
        """

        :param text: The text in the frame
        :param f_s: The style of the frame
        :param f_c: The color of the frame
        :param f_b: The background color of the frame
        :param c: The color of the text in the frame
        :param b: The background color of the text in the frame
        :param s: The style of the text in the frame
        :return:

        If no parameters are given to the frame, it will take the 'basic' style and the color and background of the text

        Frame Styles:
            - basic
            - basic2
            - single
            - double
        """

        borders = {
            'basic': {'horizontal': '-', 'vertical': '|', 'corner': '++++'},
            'basic2': {'horizontal': '=', 'vertical': '#', 'corner': '===='},
            'single': {'horizontal': '─', 'vertical': '│', 'corner': '┌┐└┘'},
            'double': {'horizontal': '═', 'vertical': '║', 'corner': '╔╗╚╝'}
        }

        border_chars = borders.get(f_s, borders['basic'])
        max_length = max(len(line.strip()) for line in text.splitlines())
        top_border = border_chars['corner'][0] + border_chars['horizontal'] * (max_length + 2) + border_chars['corner'][
            1]
        bottom_border = border_chars['corner'][2] + border_chars['horizontal'] * (max_length + 2) + border_chars['corner'][3]
        middle_border = border_chars['vertical'] + ' ' * (max_length + 2) + border_chars['vertical']

        framed_text = [AdvancedPrinter._prepare_text(top_border, foreground=f_c or c, background=f_b or b)]
        for line in text.splitlines():
            line_content = line.strip().ljust(max_length)
            colored_text = AdvancedPrinter._prepare_text(f'{line_content}', foreground=c, background=b, style=s)
            left_border = AdvancedPrinter._prepare_text(border_chars['vertical'] + ' ', foreground=f_c or c,
                                                        background=f_b or b)
            right_border = AdvancedPrinter._prepare_text(' ' + border_chars['vertical'], foreground=f_c or c,
                                                         background=f_b or b)
            colored_line = f"{left_border}{colored_text}{right_border}"
            framed_text.append(colored_line)

        if framed_text[-1] != middle_border:  # If the last line is not the middle border, append bottom border
            framed_text.append(AdvancedPrinter._prepare_text(bottom_border, foreground=f_c or c, background=f_b or b))

        final = '\n'.join(framed_text)
        print(final)

    @staticmethod
    def help():
        """
        Print out all available colors and styles.
        """
        styles = ['B', 'IT', 'U', 'INV', 'STR']

        print("Text Colors:")
        for color in dir(AdvancedPrinter.C):
            if color.isupper() and not color.startswith('BG_') and not color == 'RESET' and color not in styles:
                AdvancedPrinter.print("- {}".format(color), c=color)

        print("\nBackground Colors:")
        for color in dir(AdvancedPrinter.C):
            if color.startswith('BG_'):
                bg_color = color[3:]
                line_style = AdvancedPrinter.line('          ', b=bg_color)
                AdvancedPrinter.print("{} - {}".format(line_style, bg_color))

        print("\nAvailable styles:")
        for style in dir(AdvancedPrinter.C):
            if style.isupper() and style in styles:
                line_style = AdvancedPrinter.line("{}".format(style), s=style)
                AdvancedPrinter.print("- {}".format(line_style))
