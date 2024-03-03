/// Simple, insecure random number generator.
///
/// Taken from https://docs.oracle.com/javase/7/docs/api/java/util/Random.html
pub struct FastRandom {
    seed: u64,
}

impl FastRandom {
    pub fn new(seed: u64) -> Self {
        Self {
            seed: (seed ^ 0x5DEECE66Du64) & ((1u64 << 48) - 1),
        }
    }

    pub fn next(&mut self, bits: usize) -> u32 {
        self.seed =
            self.seed.wrapping_mul(0x5DEECE66Du64).wrapping_add(0xBu64) & ((1u64 << 48) - 1);
        (self.seed >> (48 - bits)) as u32
    }

    /// Return a value between 0 and 1.
    pub fn next_f32(&mut self) -> f32 {
        self.next(24) as f32 / (1u32 << 24) as f32
    }

    /// Return a value between [0, n)
    pub fn next_i32(&mut self, n: i32) -> i32 {
        // Power of 2
        if (n & !n) == n {
            return ((n as i64 * self.next(31) as i64) >> 31) as i32;
        }

        loop {
            let bits = self.next(31) as i32;
            let val = bits % n;

            if bits.wrapping_sub(val).wrapping_add(n).wrapping_sub(1) < 0 {
                continue;
            }

            return val;
        }
    }

    pub fn permute<T>(&mut self, slice: &mut [T]) {
        // Fisher-Yates shuffles
        let n = slice.len();
        if n < 2 {
            return;
        }
        for idx in 0..=n - 2 {
            let j = idx + self.next_i32((n - idx).try_into().unwrap()) as usize;
            slice.swap(idx, j);
        }
    }
}
