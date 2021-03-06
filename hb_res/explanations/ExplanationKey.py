from hashlib import sha224 as _hasher
from base64 import \
    urlsafe_b64encode as _encode_digest, \
    urlsafe_b64decode as _decode_digest

__author__ = 'moskupols'


class ExplanationKey:
    """
    This class, as goes from its name, encapsulates the mysterious concept of 'explanation key'.

    It can be used as hash to distinguish explanations primarily by its title and text.
    >>> from hb_res.explanations import ExplanationKey, Explanation
    >>> k = ExplanationKey.for_explanation(Explanation('альфа', '*пропуск* и омега'))
    >>> k
    <ExplanationKey "KFK1i7dgScOfKp8YvtlfSr7TrjXlEqJIuROobQ==">
    >>> k2 = ExplanationKey.for_explanation(Explanation('обед', 'синоним к слову еда'))
    >>> k == k2
    False
    >>> k3 = ExplanationKey.for_explanation(Explanation('обед', 'синоним к слову еда'))
    >>> k2 == k3
    True

    ExplanationKey provides two methods for safe saving and restoring key in str: .encode() and .decode().
    str is also available for convenience.
    >>> k.encode()
    'KFK1i7dgScOfKp8YvtlfSr7TrjXlEqJIuROobQ=='
    >>> str(k)
    'KFK1i7dgScOfKp8YvtlfSr7TrjXlEqJIuROobQ=='
    >>> k == ExplanationKey.decode(k.encode())
    True

    It is hashable and equality comparable, thus dict/set-storable.
    """

    BYTES_LENGTH = _hasher().digest_size
    ENCODED_LENGTH = len(_encode_digest(_hasher().digest()))

    def __init__(self, h: bytes):
        """
        Constructs an ExplanationKey with the given hash digest.
        The constructor shouldn't be called directly, as there is still no confidence with inner logic of the class
        and thus with proper parameters for the constructor.

        *Use ExplanationKey.for_text and ExplanationKey.encode instead*.

        :param h: BYTES_LENGTH-sized bytes object
        :raise ValueError: If len(h) != DIGEST_LENGTH
        """
        if not isinstance(h, bytes):
            raise TypeError(
                'ExplanationKey.__init__ takes bytes as parameter. Consider using .for_text or .decode instead.')

        if len(h) != self.BYTES_LENGTH:
            raise ValueError('The current used key digest size is {}, not {}'.format(self.BYTES_LENGTH, len(h)))

        self._digest = h

    @classmethod
    def for_explanation(cls, e):
        """
        Constructs an ExplanationKey for explanation e.
        It will not look at its key, even if it is not Null.

        :param e: The explanation.
        :return: A properly initialized ExplanationKey.
        """
        h = _hasher()
        for part in (e.title, '#', e.text):
            h.update(part.encode('utf-8'))
        return ExplanationKey(h.digest())

    @classmethod
    def decode(cls, r: str):
        """
        Restores ExplanationKey using previously encoded printable representation.

        :param r: str object previously got from .encode or str()
        :return: A properly initialized ExplanationKey.
        :raise ValueError: if len(r) != ENCODED_LENGTH
        """
        if len(r) != cls.ENCODED_LENGTH:
            raise ValueError('The properly encoded key\'s length is {}, not {}'.format(cls.ENCODED_LENGTH, len(r)))
        return cls(_decode_digest(r))

    def encode(self) -> str:
        """
        Encodes the key as a printable, url-safe str of length ENCODED_LENGTH. The key can be later restored using
        .decode class method.

        :return: Printable, url-safe str of length ENCODED_LENGTH
        """
        return _encode_digest(self._digest).decode()

    def __repr__(self):
        return '<ExplanationKey "{}">'.format(self.encode())

    def __str__(self)->str:
        return self.encode()

    def __hash__(self):
        return hash(self._digest)

    def __eq__(self, y):
        if isinstance(y, ExplanationKey):
            return self._digest == y._digest
        return super().__eq__(y)
