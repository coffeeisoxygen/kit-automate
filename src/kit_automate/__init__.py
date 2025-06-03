"""Automatisasi website dengan support modem pool gsm untuk sistem msisdn dan otp verifikasi."""

# fallback version if failed to import
try:
    from ._version import __version__
except ImportError:
    __version__ = "0.0.0"
