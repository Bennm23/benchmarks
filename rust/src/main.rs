use std::{fs::{File, OpenOptions}, i64, io::Write, sync::{Arc, Mutex}, thread, time::{Duration, Instant, SystemTime, UNIX_EPOCH}};

use rayon::iter::{IntoParallelIterator, ParallelIterator};

trait SynchronizedElement: Clone + Copy {}

impl SynchronizedElement for u128 {}
impl SynchronizedElement for f64 {}

#[derive(Clone)]
struct SynchronizedList <T> 
{
    _backed: Arc<Mutex<Vec<T>>>,
}

impl <T: SynchronizedElement> SynchronizedList<T> 
{

    pub fn new() -> Self {
        Self {
            _backed: Arc::new(Mutex::new(Vec::new())),
        }
    }

    pub fn push(&self, element: T) {
        
        let guard = self._backed.lock();

        match guard {
            Ok(mut data) => {
                data.push(element);
            },
            Err(e) => {
                println!("Failed To Push to List Due to {e}");
            }
        }
    }
}

fn arithmetic_deltas() {
    let mut deltas: Vec<u128> = Vec::new();
    // sum += 12345000.5;
    // sum *= 103.12;
    // long si = (long) sum % Long.MAX_VALUE;
    // si /= 543212345;


    for _ in 0..100_000 {
        let start = Instant::now();
        let mut sum = 0f64;
        sum += 12345000.5;
        sum *= 103.12;
        let mut si = sum as i64 % i64::MAX;
        si /= 543212345;
        deltas.push(start.elapsed().as_nanos());
    }
    let mut arithmetic_file = open_and_clear_file(ARITHMETIC_DELTAS_PATH);

    for entry in deltas {
        writeln!(arithmetic_file, "{:.4}", entry).expect("File Write Failed");
    }

}

fn main() {
    println!("Hello, world!");

    arithmetic_deltas();
    // build_deltas();
}

const NUM_DELTAS: usize = 10000;
const DELTAS_PATH: &str = "/home/benn/CODE/PerformanceAnalysis/delta_outs/rust_out.txt";
const SYS_DELTAS_PATH: &str = "/home/benn/CODE/PerformanceAnalysis/delta_outs/rust_out_sys.txt";
const ARITHMETIC_DELTAS_PATH: &str = "/home/benn/CODE/PerformanceAnalysis/delta_outs/rust_out_arithmetic.txt";

fn open_and_clear_file(path: &str) -> File {
    {
        OpenOptions::new()
            .create(true)
            .write(true)
            .truncate(true)
            .open(path)
            .expect("Failed to open deltas file");
    }
    OpenOptions::new()
        .append(true)
        .open(path)
        .expect("Failed to open deltas file")
}

fn get_system_time_nanos() -> u128 {
    SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_nanos()
}

fn build_deltas() {

    let deltas: SynchronizedList<u128> = SynchronizedList::new();
    let sys_deltas: SynchronizedList<f64> = SynchronizedList::new();

    const SLEEP_DURATION: Duration = Duration::from_millis(1);

    (0..NUM_DELTAS).into_par_iter().for_each(|_i| {

        let sys_start = get_system_time_nanos();
        let start = Instant::now();
        thread::sleep(SLEEP_DURATION);

        let elapsed_nanos = start.elapsed().as_nanos() - SLEEP_DURATION.as_nanos();
        let sys_end = get_system_time_nanos();
        let sys_total = (sys_end - sys_start) as f64 / 1000.0 - 1000.0;
        deltas.push(elapsed_nanos);
        sys_deltas.push(sys_total);
    });

    let opt = deltas._backed.lock().unwrap();

    let mut file = open_and_clear_file(DELTAS_PATH);

    for entry in opt.iter() {
        writeln!(file, "{}", entry).expect("File Write Failed");
    }

    let opt = sys_deltas._backed.lock().unwrap();

    let mut sys_file = open_and_clear_file(SYS_DELTAS_PATH);

    for entry in opt.iter() {
        writeln!(sys_file, "{:.4}", entry).expect("File Write Failed");
    }
}
