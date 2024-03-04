class Console:
    def info(self, message, end=None):
        """Prints an informational message in blue color."""
        print("\033[94m" + f"{message}" + "\033[0m", end=end)

    def warn(self, message, end=None):
        """Prints a warning message in yellow color."""
        print("\033[93m" + f"{message}" + "\033[0m", end=end)

    def error(self, message, end=None):
        """Prints an error message in red color."""
        print("\033[91m" + f"{message}" + "\033[0m", end=end)

    def success(self, message, end=None):
        """Prints a success message in green color."""
        print("\033[92m" + f"{message}" + "\033[0m", end=end)

    def secondary(self, message, end=None):
        """Prints a secondary message in gray color."""
        print("\033[90m" + f"{message}" + "\033[0m", end=end)
