import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.*;

public class TimedCollapsedGibbs {
    /*
        d       : document index
        C_d     : {A, S},
                  where A: ACL, S: NIPS
        w_{d,i} : words set index
        V       : total number of word
        v       : indexes the v-th word in the vocabulary
        K       : total topics
        phi_k   : global parameter
        phi_k^c : collection parameter
        theta_d : mixing proportions for the topics in document d
        N_d     : the number of words in the document d
        Z_{d,i} : topic index, sampled from Mult(theta_d)
        lambda  : the probability that the word w_{d,i} is sampled according to the collection-specific distribution phi_k^c
        x_{d,i} : binary random variable, whether to use phi or phi^c
                  x is a Bernoulli random variable with parameter lambda
        alpha, beta, lambda : are hyperparameters that is the parameter of prior distribution
     */

    private int _k;
    private int _col;  //number of collection;
    private int _v;    //total number of unique word types
    private Map<String, Integer> _wType; //word types
    private double _lambda;
    private double _alpha;
    private double _beta;

    //counters
    private int[][] _ndk;  //the number of tokens in document d assigned to topic k
    private int[] _nds;    //the number of tokens assigned to any topic in document d (the length of document d)
    private int[][] _nkw;  //the number of tokens assigned to topic k which are the word type w (x = 0)
    private int[] _nks;    //the total number of tokens of any word type that are assigned to topic k
    private int[][][] _nckw; //the corpus-dependent counts (x = 1)
    private int[][] _ncks;
    private int[][] _testNdk;
    private int[] _testNds;

    //parameters
    private double[][] _thetadk;
    private double[][] _phikw;
    private double[][][] _phickw;
    private double[][] _testThetadk;

    public TimedCollapsedGibbs() {
        this._wType = new HashMap<String, Integer>();
    }

    //perform collapse Gibb sampling
    public void sampling(String trainFile, String testFile, String outputFile, int k, double lambda, double alpha, double beta, int iterNum, int biNum) throws IOException {
        _k = k;
        _alpha = alpha;
        _beta = beta;
        _lambda = lambda;

        //parse training and testing documents
        List<String[]> trainData = parseDoc(trainFile, true);
        List<String[]> testData  = parseDoc(testFile, false);

        //count vocabulary
        int vocabIdx = 0;
        vocabIdx = countVocab(trainData, vocabIdx);
        vocabIdx = countVocab(testData, vocabIdx);

        //initialize counters
        _ndk     = new int[trainData.size()][k];
        _nds     = new int[trainData.size()];
        _nkw     = new int[k][_wType.size()];
        _nks     = new int[k];
        _nckw    = new int[_col][k][_wType.size()];
        _ncks    = new int[_col][k];
        _testNdk = new int[testData.size()][k];
        _testNds = new int[testData.size()];
        _v = _wType.size();

        //initialize parameters
        _thetadk = new double[trainData.size()][k];
        _phikw   = new double[k][_v];
        _phickw  = new double[_col][k][_v];
        _testThetadk = new double[trainData.size()][k];

        //for collecting samples after burn-in period
        List<double[][]> thetadkSample  = new ArrayList<double[][]>();
        List<double[][]> phikwSample    = new ArrayList<double[][]>();
        List<double[][][]> phickwSample = new ArrayList<double[][][]>();

        //for collecting log likelihood for each iteration
        List<Double> logLikelihoodTrain = new ArrayList<Double>();
        List<Double> logLikelihoodTest = new ArrayList<Double>();
        long[] timeStamp = new long[iterNum];

        //randomly initialize z and x
        Random rand = new Random(0);
        int[][] zdi = initZX(trainData, k, rand);
        int[][] xdi = initZX(trainData, 2, rand);
        int[][] testZdi = initZX(testData, k, rand);
        int[][] testXdi = initZX(testData, 2, rand);

        //do counting
        countN(trainData, zdi, xdi);
        countTestNdk(testData, testZdi, testXdi);


        //================================================================
        //perform sampling process for iterNum iterations
        //================================================================
        long startTime = System.nanoTime();
        for(int t = 1; t <= iterNum; t++) {
            if (t % 10 == 0)
                System.out.printf("%d-th iteration...\n", t);

            for(int d = 0; d < trainData.size(); d++) {
                String[] doc = trainData.get(d);
                for(int i = 1; i < doc.length; i++) {
                    excludeCnt(d, i, doc, xdi, zdi);
                    zdi[d][i] = sampleZdi(d, i, xdi, doc);
                    xdi[d][i] = sampleXdi(d, i, zdi, doc);
                    includeCnt(d, i, doc, xdi, zdi);
                }
            }

            _thetadk = estimateTheta(trainData, _thetadk, _ndk, _nds); //TODO: start check here
            estimatePhi();

            //after burn-in period, collect samples
            if (t > biNum) {
                thetadkSample.add(copyArray2(_thetadk));
                phikwSample.add(copyArray2(_phikw));
                phickwSample.add(copyArray3(_phickw));
            }

            //sample z and x for the test set
            for(int d = 0; d < testData.size(); d++) {
                String[] doc = testData.get(d);
                for(int i = 1; i < doc.length; i++) {
                    excludeTestCnt(d, i, doc, testXdi, testZdi);
                    testZdi[d][i] = sampleTestZdi(d, i, testXdi, doc);
                    testXdi[d][i] = sampleTestXdi(d, i, testZdi, doc);
                    includeTestCnt(d, i, doc, testXdi, testZdi);
                }
            }

            _testThetadk = estimateTheta(testData, _testThetadk, _testNdk, _testNds);

            //compute log-likelihood
            logLikelihoodTrain.add(computeLogLikelihood(trainData, _thetadk, xdi));
            logLikelihoodTest.add(computeLogLikelihood(testData, _testThetadk, testXdi));
            timeStamp[t-1] = (System.nanoTime() - startTime) / 1000000;  //divide by 1000000 to get milliseconds.
        }

        outputData(outputFile, thetadkSample, phikwSample, phickwSample, logLikelihoodTrain, logLikelihoodTest);
        outputTime(timeStamp, outputFile);

    }

    private double[][] copyArray2(double[][] org) {
        double[][] nAry = new double[org.length][];
        for(int i = 0; i < org.length; i++) {
            nAry[i] = Arrays.copyOf(org[i], org[i].length);
        }
        return nAry;
    }

    private double[][][] copyArray3(double[][][] org) {
        double[][][] nAry = new double[org.length][][];
        for(int i = 0; i < org.length; i++) {
            nAry[i] = new double[org[i].length][];
            for(int j = 0; j < org[i].length; j++) {
                nAry[i][j] = Arrays.copyOf(org[i][j], org[i][j].length);
            }
        }
        return nAry;
    }

    private double computeLogLikelihood(List<String[]> data, double[][] thetadk, int[][] xdi) {
        double logProb = 0.0;
        for(int d = 0; d < data.size(); d++) {
            String[] doc = data.get(d);
            int c = Integer.valueOf(doc[0]);
            for(int i = 1; i < doc.length; i++) {
                double thetaProb = 0.0;
                int w = _wType.get(doc[i]);
                for(int kk = 0; kk < _k; kk++) {
                    thetaProb += thetadk[d][kk] * ((1 - _lambda) * _phikw[kk][w] + _lambda * _phickw[c][kk][w]);
                }
                logProb += Math.log(thetaProb);
            }
        }
        return logProb;
    }

    private int sampleZdi(int d, int i, int[][] xdi, String[] doc) {
        int c = Integer.valueOf(doc[0]);
        int w = _wType.get(doc[i]);
        double[] prob = new double[_k];
        for(int kk = 0; kk < _k; kk++) {
            if (xdi[d][i] == 0) {
                prob[kk] = (_ndk[d][kk] + _alpha) * (_nkw[kk][w] + _beta) /
                        ( (_nds[d] + _k * _alpha) * (_nks[kk] + _v * _beta) );
            } else {
                prob[kk] = (_ndk[d][kk] + _alpha) * (_nckw[c][kk][w] + _beta) /
                        ( (_nds[d] + _k * _alpha) * (_ncks[c][kk]) + _v * _beta );
            }
        }
        return weightedRandom(prob);
    }

    private int sampleTestZdi(int d, int i, int[][] xdi, String[] doc) {
        int c = Integer.valueOf(doc[0]);
        int w = _wType.get(doc[i]);
        double[] prob = new double[_k];
        for(int kk = 0; kk < _k; kk++) {
            if (xdi[d][i] == 0) {
                prob[kk] = (_testNdk[d][kk] + _alpha) * _phikw[kk][w] / (_testNds[d] + _k * _alpha);
            } else {
                prob[kk] = (_testNdk[d][kk] + _alpha) * _phickw[c][kk][w] / (_testNds[d] + _k * _alpha);
            }
        }
        return weightedRandom(prob);
    }

    private int sampleXdi(int d, int i, int[][] zdi, String[] doc) {
        int c = Integer.valueOf(doc[0]);
        int w = _wType.get(doc[i]);
        int k = zdi[d][i];
        double wdi0 = (1 - _lambda) * (_nkw[k][w] + _beta) / (_nks[k] + _v * _beta);
        double wdi1 = _lambda * (_nckw[c][k][w] + _beta) / (_ncks[c][k] + _v * _beta);

        double pick = Math.random() * (wdi0 + wdi1);
        if (pick <= wdi0) {
            return 0;
        } else {
            return 1;
        }
    }

    private int sampleTestXdi(int d, int i, int[][] zdi, String[] doc) {
        int w = _wType.get(doc[i]);
        int k = zdi[d][i];
        int c = Integer.valueOf(doc[0]);
        double wdi0 = (1 - _lambda) * _phikw[k][w];
        double wdi1 = _lambda * _phickw[c][k][w];

        double pick = Math.random() * (wdi0 + wdi1);
        if (pick <= wdi0) {
            return 0;
        } else {
            return 1;
        }
    }

    private int weightedRandom(double[] prob) {
        double tot = 0.0;
        for (double p : prob) {
            tot += p;
        }
        double pick = Math.random() * tot;
        double cumu = 0.0;
        for(int i = 0; i < prob.length; i++) {
            cumu += prob[i];
            if (pick <= cumu) {
                return i;
            }
        }
        return prob.length - 1;
    }

    private void excludeCnt(int d, int i, String[] doc, int[][] xdi, int[][] zdi) {
        int c = Integer.valueOf(doc[0]);
        int w = _wType.get(doc[i]);
        int k = zdi[d][i];
        _ndk[d][k] -= 1;
        _nds[d] -= 1;
        _nkw[k][w] -= 1;
        _nks[k] -= 1;
        _nckw[c][k][w] -= 1;
        _ncks[c][k] -= 1;
    }

    private void excludeTestCnt(int d, int i, String[] doc, int[][] xdi, int[][] zdi) {
        int k = zdi[d][i];
        _testNdk[d][k] -= 1;
        _testNds[d] -= 1;
    }

    private void includeCnt(int d, int i, String[] doc, int[][] xdi, int[][] zdi) {
        int c = Integer.valueOf(doc[0]);
        int w = _wType.get(doc[i]);
        int k = zdi[d][i];
        _ndk[d][k] += 1;
        _nds[d] += 1;
        _nkw[k][w] += 1;
        _nks[k] += 1;
        _nckw[c][k][w] += 1;
        _ncks[c][k] += 1;
    }

    private void includeTestCnt(int d, int i, String[] doc, int[][] xdi, int[][] zdi) {
        int k = zdi[d][i];
        _testNdk[d][k] += 1;
        _testNds[d] += 1;
    }

    private double[][] estimateTheta(List<String[]> docs, double[][] theta, int[][] ndk, int[] nds) {
        double div;
        for (int d = 0; d < docs.size(); d++) {
            div = nds[d] + _k * _alpha;
            for (int kk = 0; kk < _k; kk++) {
                theta[d][kk] = (ndk[d][kk] + _alpha) / div;
            }
        }
        return theta;
    }

    private void estimatePhi() {
        for(int kk = 0; kk < _k; kk++) {
            for(int w = 0; w < _v; w++) {
                _phikw[kk][w] = (_nkw[kk][w] + _beta) / (_nks[kk] + _v * _beta);
                for(int c = 0; c < _col; c++) {
                    _phickw[c][kk][w] = (_nckw[c][kk][w] + _beta) / (_ncks[c][kk] + _v * _beta);
                }
            }
        }
    }

    private void countN(List<String[]> data, int[][] zdi, int[][] xdi) {
        for(int d = 0; d < data.size(); d++) {
            String[] doc = data.get(d);
            int c = Integer.valueOf(doc[0]);

            _nds[d] = doc.length - 1;  //extract 1 for the first collection tag
            for(int i = 1; i < doc.length; i++) {
                int w = _wType.get(doc[i]);
                int k = zdi[d][i];
                _ndk[d][k] += 1;
                _nks[k] += 1;
                _nkw[k][w] += 1;
                _nckw[c][k][w] += 1;
                _ncks[c][k] += 1;
            }
        }
    }

    private void countTestNdk(List<String[]> data, int[][] zdi, int[][] xdi) {
        for(int d = 0; d < data.size(); d++) {
            String[] doc = data.get(d);

            for(int i = 1; i < doc.length; i++) {
                _testNdk[d][zdi[d][i]] += 1;
            }
        }
    }

    /*
     Initialize z_{d,i} value to randomly chosen values in {0, ..., k - 1}
     ..         x_{d,i} ...                                {0, 1}
     */
    private int[][] initZX(List<String[]> data, int range, Random rand) {
        int[][] res = new int[data.size()][];
        rand = new Random(0);
        for(int i = 0; i < data.size(); i++) {
            String[] s = data.get(i);
            res[i] = new int[s.length];
            for(int j = 0; j < res[i].length; j++) {
                res[i][j] = rand.nextInt(range);
            }
        }
        return res;
    }

    private int countVocab(List<String[]> docs, int idx) {
        for(String[] d : docs) {
            for(int i = 1; i < d.length; i++) {
                if(!_wType.containsKey(d[i])){
                    _wType.put(d[i], idx);
                    idx++;
                }
            }
        }
        return idx;
    }

    /*
     Read data line by line and split the string into list of words.
     Find the total number of collection by looking at the first item in each string.
     */
    private List<String[]> parseDoc(String file, boolean update) throws IOException {
        List<String[]> data = new ArrayList<String[]>();
        Set<String> coll = new HashSet<String>();
        BufferedReader br = new BufferedReader(new FileReader(file));
        String line;
        int index = 0;
        while ((line = br.readLine()) != null) {
            String[] s = line.split(" ");
            data.add(s);

            if (update) {
                coll.add(s[0]); //update collection set
            }
        }

        if (update) {
            this._col = coll.size();
        }

        return data;
    }



    /*
     output files:
       outputFile.txt-theta   : contains the values of theta for the training data
       outputFile.txt-phi     : contains the values of phi.
       outputFile.txt-phi0    : contains the values of phi^(0)
       outputFile.txt-phi1    : contains the values of phi^(1)
       outputFile.txt-trainll : contains the log-likelihoods on the training data for each iteration
       outputFile.txt-testll  : contains the log-likelihoods on the test data for each iteration
     */
    private void outputData(String outputFile, List<double[][]> thetadk, List<double[][]> phikw, List<double[][][]> phickw, List<Double> llTrain, List<Double> llTest) throws IOException {
        //output theta
        String oTheta = outputFile + "-theta";
        outputTheta(thetadk, oTheta);

        //output phi
        String oPhi = outputFile + "-phi";
        outputPhis(phikw, phickw, oPhi);

        //output log likelihood
        String llTrainFile = outputFile + "-trainll";
        outputLogLikelihood(llTrain, llTrainFile);
        String llTestFile = outputFile + "-testll";
        outputLogLikelihood(llTest, llTestFile);
    }

    /*
     Output average theta for each document d and each topic k
     */
    private void outputTheta(List<double[][]> thetadk, String file) throws IOException {
        //initialize avgTheta
        double[][] first = thetadk.get(0);
        double[][] avgTheta = new double[first.length][];
        for(int d = 0; d < first.length; d++){
            avgTheta[d] = new double[first[d].length];
        }

        //sum over all theta
        for(double[][] th : thetadk) {
            for(int d = 0; d < th.length; d++) {
                for(int i = 0; i < th[d].length; i++) {
                    avgTheta[d][i] += th[d][i];
                }
            }
        }

        //write to file
        StringBuilder sb = new StringBuilder();
        try {
            String line = "%.13e ";
            for(int d = 0; d < avgTheta.length; d++) {
                for(int i = 0; i < avgTheta[d].length; i++) {
                    sb.append(String.format(line, avgTheta[d][i] / avgTheta.length));
                }
                sb.append("\n");
            }
            Path path = Paths.get(file);
            BufferedWriter writer = Files.newBufferedWriter(path);
            writer.write(sb.toString());
            writer.close();

        } catch (IOException e) {
            e.printStackTrace();
        }
    }


    /*
     Output average phi for each topic k and word w.
     Also output corpus-dependent parameters phi0 and phi1.
     */
    private void outputPhis(List<double[][]> phikw, List<double[][][]> phickw, String file) throws IOException {
        //output phi
        outputPhi(phikw, file);

        //
        String outputPhi0 = file + "0";
        String outputPhi1 = file + "1";
        List<double[][]> phi0 = new ArrayList<double[][]>();
        List<double[][]> phi1 = new ArrayList<double[][]>();
        for(int d = 0; d < phickw.size(); d++) {
            double[][][] pckw = phickw.get(d);
            phi0.add(pckw[0]);
            phi1.add(pckw[1]);
        }

        //output phi0 and phi1
        outputPhi(phi0, outputPhi0);
        outputPhi(phi1, outputPhi1);
    }

    /*
     output average phi.
     */
    private void outputPhi(List<double[][]> phi, String file) throws IOException {
        //initialize avgPhi
        double[][] first = phi.get(0);
        double[][] avgPhi = new double[first.length][];
        for(int d = 0; d < first.length; d++){
            avgPhi[d] = new double[first[d].length];
        }

        //sum over all phi
        for(double[][] ph : phi) {
            for(int k = 0; k < ph.length; k++) {
                for(int w = 0; w < ph[k].length; w++) {
                    avgPhi[k][w] += ph[k][w];
                }
            }
        }

        //write to file
        try {
            StringBuilder sb = new StringBuilder();
            String line = "%.13e ";
            for(Map.Entry<String, Integer> w : _wType.entrySet()){
                sb.append(w.getKey());
                sb.append(" ");
                for(int k = 0; k < _k; k++) {
                    sb.append(String.format(line, avgPhi[k][w.getValue()] / avgPhi.length));
                }
                sb.append("\n");
            }
            Path path = Paths.get(file);
            BufferedWriter writer = Files.newBufferedWriter(path);
            writer.write(sb.toString());
            writer.close();

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void outputLogLikelihood(List<Double> lldata, String file) throws IOException {
        try {
            StringBuilder sb = new StringBuilder();
            String line = "%.13e\n";
            for(double d : lldata) {
                sb.append(String.format(line, d));
            }
            Path path = Paths.get(file);
            BufferedWriter writer = Files.newBufferedWriter(path);
            writer.write(sb.toString());
            writer.close();

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void outputTime(long[] timeStamp,  String file) throws IOException {
        String fileName = file + "-time";

        StringBuilder sb = new StringBuilder();
        String line = "%d\n";
        for(long t : timeStamp) {
            sb.append(String.format(line, t));
        }

        try {
            Path path = Paths.get(fileName);
            BufferedWriter writer = Files.newBufferedWriter(path);
            writer.write(sb.toString());
            writer.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) throws IOException {
        String trainFile  = args[0];
        String testFile   = args[1];
        String outputFile = args[2];
        int k             = Integer.valueOf(args[3]);  //topic number
        double lambda     = Double.valueOf(args[4]);
        double alpha      = Double.valueOf(args[5]);
        double beta       = Double.valueOf(args[6]);
        int iterNum       = Integer.valueOf(args[7]);  //total iterations
        int biNum         = Integer.valueOf(args[8]);  //burn-in period

        TimedCollapsedGibbs tcg = new TimedCollapsedGibbs();
        try {
            tcg.sampling(trainFile, testFile, outputFile, k, lambda, alpha, beta, iterNum, biNum);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
