use std::cell::UnsafeCell;

/// An UnsafeCell that allows for racy access as well.
///
/// This is very unsafe as the Rust compiler presumes a lot more about references.
pub struct UnsafeSync<'a, T> {
    value: &'a mut UnsafeCell<T>,
}

unsafe impl<'a, T> Sync for UnsafeSync<'a, T> {}
unsafe impl<'a, T> Send for UnsafeSync<'a, T> {}

impl<'a, T> From<&'a mut T> for UnsafeSync<'a, T> {
    fn from(value: &'a mut T) -> Self {
        Self {
            value: UnsafeCell::from_mut(value),
        }
    }
}

impl<'a, T> UnsafeSync<'a, T> {
    /// Returns a mutable reference to the underlying data.
    #[allow(dead_code)]
    pub fn get_mut(&'a mut self) -> &'a mut T {
        self.value.get_mut()
    }

    /// Unsafely get a mutable reference to the underlying data.
    ///
    /// Unlike get_mut, uget does not check at all that the reference is unique.
    #[allow(clippy::mut_from_ref)]
    pub unsafe fn uget(&'a self) -> &'a mut T {
        &mut *self.value.get()
    }
}
