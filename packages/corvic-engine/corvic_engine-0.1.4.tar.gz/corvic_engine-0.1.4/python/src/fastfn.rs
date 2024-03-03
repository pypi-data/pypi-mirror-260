const SIGMOID_TABLE_SIZE: usize = 1000;
const SIGMOID_MAX_EXP: f32 = 6.;
static mut SIGMOID_TABLE: [f32; SIGMOID_TABLE_SIZE] = [0.; SIGMOID_TABLE_SIZE];

/// sigmoid(x) = 1 / (exp(-x) + 1)
pub fn init_sigmoid_table() {
    unsafe {
        for (i, entry) in SIGMOID_TABLE.iter_mut().enumerate() {
            let p = i as f64 / SIGMOID_TABLE_SIZE as f64 * 2. - 1.;
            let exp = (p * SIGMOID_MAX_EXP as f64).exp();
            let value = exp / (exp + 1.);
            *entry = value as f32;
        }
    }
}

pub fn sigmoid(x: f32) -> Option<f32> {
    if x <= -SIGMOID_MAX_EXP || x >= SIGMOID_MAX_EXP {
        return None;
    }
    let p = (x + SIGMOID_MAX_EXP) * (SIGMOID_TABLE_SIZE as f32 / SIGMOID_MAX_EXP / 2.);
    Some(*unsafe { SIGMOID_TABLE.get_unchecked(p as usize) })
}
