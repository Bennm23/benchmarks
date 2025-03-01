import java.io.FileWriter;
import java.io.IOException;
import java.time.Instant;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.stream.IntStream;

public class Main {

    static final String SYS_DELTAS_PATH = "/home/benn/CODE/PerformanceAnalysis/delta_outs/java_out_sys.txt";
    static final String DELTAS_PATH = "/home/benn/CODE/PerformanceAnalysis/delta_outs/java_out.txt";
    static final String ARITHMETIC_DELTAS_PATH = "/home/benn/CODE/PerformanceAnalysis/delta_outs/java_out_arithmetic.txt";
    public static double instant_delta_micros(Instant start, Instant end) {
        long secondDelta = end.getEpochSecond() - start.getEpochSecond();
        long nanoDelta = end.getNano() - start.getNano();

        return nanoDelta / 1_000.0 + secondDelta * 1_000_000.0;
    }

    public static void arithmeticDeltas() throws IOException {
        List<Long> deltas = new ArrayList<>();
        for (int i = 0; i < 100_000; i++) {
            var start = System.nanoTime();
            double sum = 0;
            sum += 12345000.5;
            sum *= 103.12;
            long si = (long) sum % Long.MAX_VALUE;
            si /= 543212345;
            var end = System.nanoTime();
            deltas.add(end - start); // Get Delta in Nano Time vs Expected
        }

//        IntStream.range(0, 100)
//                .parallel()
//                .forEach(_i -> {
//
//                    var start = System.nanoTime();
//                    for (int i = 0; i < 100_000; i++) {
//                        double sum = 0;
//                        sum += 12345.5;
//                        sum *= 103.12;
//                        long si = (long) sum % Long.MAX_VALUE;
//                    }
//                    var end = System.nanoTime();
//                    deltas.add(end - start); // Get Delta in Nano Time vs Expected
//                });
        writeDataToFile(deltas, ARITHMETIC_DELTAS_PATH, (d) -> String.format("%d\n", d));
    }

    public static void main(String[] args) throws IOException {
//        sleepDeltas();
        arithmeticDeltas();
    }
    public static void sleepDeltas() throws IOException {
        List<Long> deltas = Collections.synchronizedList(new ArrayList<>());
        List<Double> sys_deltas = Collections.synchronizedList(new ArrayList<>());
        final long expected_delta_nanos = 1_000_000;

        IntStream.range(0, 10000)
                .parallel()
                .forEach(i -> {
                    var sys_start = Instant.now();
                    var start = System.nanoTime();
                    try {
                        Thread.sleep(1);
                    } catch (InterruptedException ignored) {}
                    var end = System.nanoTime();
                    var sys_end = Instant.now();
                    deltas.add(end - start - expected_delta_nanos); // Get Delta in Nano Time vs Expected
                    sys_deltas.add(instant_delta_micros(sys_start, sys_end) - 1000.0); // Get Delta in System Time vs Expected
                });

        writeDataToFile(deltas, DELTAS_PATH, (d) -> String.format("%d\n", d));
        writeDataToFile(sys_deltas, SYS_DELTAS_PATH, (f) -> String.format("%.4f\n", f));

    }
    interface IConverter <T extends Number> {
        String convert(T num);
    }
    public static <T extends Number> void writeDataToFile(List<T> data, String file, IConverter<T> converter) throws IOException {
        try (FileWriter fw = new FileWriter(file, false)) {
            fw.write("");
        }

        try (FileWriter fw = new FileWriter(file, true)) {
            data.forEach(delta -> {
                try {
                    fw.write(converter.convert(delta));
                } catch (IOException e) {
                    e.printStackTrace();
                }
            });
        }
    }
}