import numpy as np

# TODO: implement dynamic dtype

def downshift(bdata: np.ndarray, shift: int) -> np.ndarray:
    return np.sign(bdata) * (np.abs(bdata) >> shift)


class fptarrau(np.ndarray):
    """
    Data type for fixed-point binary arithmetic.

    :param bw: Bit width of the fixed point type.
    :param bp: Location of the binary point starting from the lsb.
    :param data: Numpy array containing data.
    :param disbin: Flag indicating whether the data is already converted to binary.
    """

    def __new__(cls, data: np.ndarray, bw: int, bp: int, disbin: bool = False, dtype=np.int32):
        obj = np.asarray(data, dtype=dtype).view(cls)
        obj.bw = bw
        obj.bp = bp

        if not disbin:
            obj = np.around(obj * 2 ** obj.bp).astype(dtype)
            obj.mask_bitwidth()

    def __init__(self, bw: int, bp: int, data: np.ndarray = None, disbin: bool = False):
        self.bw = bw
        self.bp = bp
        if disbin or data is None:
            self.bdata = data
        else:
            self.bdata = self.from_float(data)

    def __getitem__(self, item):
        print(item)
        return FixedPointType(self.bw, self.bp, self.bdata[item.start:item.stop:item.step], disbin=True)

    def __add__(self, obj: 'FixedPointType') -> 'FixedPointType':
        """
        Return a new FixedPointType type resulting from summing this type with the provided one,
        including the carry bit.
        """
        whole_bits = max([self.bw - self.bp, obj.bw - obj.bp])
        bp = max([self.bp, obj.bp])
        bw = bp + whole_bits + 1
        return FixedPointType(bw, bp, self.bdata + obj.bdata, disbin=True)

    def __mul__(self, obj: 'FixedPointType') -> 'FixedPointType':
        """
        Return a new FixedPointType type resulting from multiplying this type with the provided one.
        """
        bw = self.bw + obj.bw
        bp = self.bp + obj.bp
        return FixedPointType(bw, bp, self.bdata * obj.bdata, disbin=True)

    def __repr__(self):
        return f"FixedPointType({self.bw}, {self.bp})"

    @property
    def data(self):
        return self.to_float()

    @property
    def shape(self):
        return self.bdata.shape

    def mask_bitwidth(self):
        """
        Truncates data from the left to mask bitwidth.
        """
        mask = (1 << self.bw) - 1
        return np.sign(self) * (np.abs(self) & mask)

    def _downshift(self, shift: int):
        self.bdata = downshift(self.bdata, shift)

    def _upshift(self, shift: int):
        self.bdata = self.bdata << shift

    def to_float(self, bdata: np.ndarray = None) -> np.ndarray:
        """
        Convert the contained binary array into its floating-point value according to the bit width and
        binary point of this data type.
        """
        if bdata is None:
            bdata = self.mask_bitwidth()
        return bdata.astype(float) / 2 ** self.bp

    def from_float(self, data):
        """
        Convert the provided floating point number or numpy array into
        its fixed-point representation according to the bit width and
        binary point of this data_ type.
        """
        if self.bw > 32:
            dtype = np.int64
        else:
            dtype = np.int32
        _bdata = np.around(data * 2 ** self.bp).astype(dtype)
        return self.mask_bitwidth(_bdata)

    def copy(self):
        return FixedPointType(self.bw, self.bp, self.bdata, disbin=True)

    @classmethod
    def cast(cls, bw: int, bp: int, obj: "FixedPointType", keep_lsb: bool = False) -> "FixedPointType":
        """
        Cast the provided FixedPointType into a new one with specified bit width and binary point.
        Casting happens in two steps:
        1. Up- or downshifting based on the new bit width (skipped if keep_lsb is True)
        2. Truncating from the left

        :param bw: Bit width of the fixed point type.
        :param bp: Location of the binary point starting from the lsb.
        :param obj: The old FixedPointType to cast.
        :param keep_lsb: If True, keeps lsb instead of msb
        """
        dtype = np.int64 if bw > 32 else np.int32
        new_obj = cls(bw, bp, obj.bdata.astype(dtype), disbin=True)

        if not keep_lsb:
            if obj.bp > bp:
                new_obj._downshift(obj.bp - bp)
            else:
                new_obj._upshift(bp - obj.bp)

        new_obj.bdata = new_obj.mask_bitwidth()
        return new_obj

    def truncate(self, bw):
        """
        Truncate the FixedPointType to a new specified bit width. The current bit width will not be replaced if the new
        value is larger. The relative position of the fixed point is preserved.

        :param bw: New bit width of the fixed point type
        """
        shift = self.bw - bw
        self._downshift(shift)
        self.bp = self.bp - shift
        if self.bp < 0:
            self.bp = 0
        self.bw = bw

    def _round(self, bw: int):
        shift = self.bw - bw
        rnd_data = downshift(self.bdata, shift) << shift
        rnd_off = self.bdata - rnd_data
        rnd_off = downshift(rnd_off, shift - 1)
        self.truncate(bw)
        return rnd_off

    def round_from_zero(self, bw: int):
        """
        Round the FixedPointType to a new specified bit width. This implements a round to nearest with ties away
        from zero. The current bit width will not be replaced if the new value is larger. The relative position
        of the fixed point is preserved.

        :param bw: New bit width of the fixed point type
        """
        rnd_off = self._round(bw)
        self.bdata += rnd_off
        self.bdata = self.mask_bitwidth()

    def round_to_even(self, bw: int):
        """
        Round the FixedPointType to a new specified bit width. This implements a round to nearest with ties to
        nearest even. The current bit width will not be replaced if the new value is larger. The relative position
        of the fixed point is preserved.

        :param bw: New bit width of the fixed point type
        """
        rnd_off = self._round(bw)
        self.bdata = np.where(self.bdata % 2 == 1, self.bdata + rnd_off, self.bdata)  # only round up odd values
        self.bdata = self.mask_bitwidth()

    def reinterpret(self, bw: int, bp: int):
        """
        Reinterprets existing FixedPointType data to new bit width and binary point without truncating on the left.

        :param bw: New bit width
        :param bp: New binary point location
        """
        if self.bw > bw:
            self._downshift(self.bw - bw)
        else:
            self._upshift(bw - self.bw)

        if self.bw <= 32:
            self.bdata = self.bdata.astype(np.int32)

        self.bw, self.bp = bw, bp

    def shift_insert(self, bdata: np.ndarray):
        if bdata.shape != self.bdata[:, 0].shape:
            raise ValueError(f"Passed data does not fit the expected shape of {self.bdata[:, 0].shape}")
        self.bdata[:, 1:] = self.bdata[:, :-1]
        self.bdata[:, 0] = bdata

    def sum(self, axis=None):
        """
        Sums the data along the give axis by simulating step-bey-step addition. The number of hardware addition
        operations would be ceil(log2(n_elements))
        """
        shape1 = self.bdata.shape
        self.bdata = self.bdata.sum(axis=axis)
        shape2 = self.bdata.shape
        print("Sum shapes", shape1, shape2)
