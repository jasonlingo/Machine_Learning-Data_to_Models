import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Random;

public class TimedBlockCollapsedGibbs extends BlockCollapsedGibbs {
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

    public TimedBlockCollapsedGibbs() {
        this._wType = new HashMap<String, Integer>();
    }

    //perform collapse Gibb sampling
    @Override
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
        _testThetadk = new double[testData.size()][k];

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
        int[][] xdi = initZX(trainData, X_RANGE, rand);
        int[][] testZdi = initZX(testData, k, rand);
        int[][] testXdi = initZX(testData, X_RANGE, rand);

        //do counting
        countN(trainData, zdi);
        countTestNdk(testData, testZdi);


        //================================================================
        //perform sampling process for iterNum iterations
        //================================================================
        long startTime = System.nanoTime();
        for(int t = 1; t <= iterNum; t++) {
//            if (t % 10 == 0)
//                System.out.printf("%d-th iteration...\n", t);
            int[] tempZXdi;
            for(int d = 0; d < trainData.size(); d++) {
                String[] doc = trainData.get(d);
                for(int i = 1; i < doc.length; i++) {
                    excludeCnt(d, i, doc, zdi);
                    tempZXdi = sampleZXdi(d, i, doc);
                    zdi[d][i] = tempZXdi[1];
                    xdi[d][i] = tempZXdi[0];
                    includeCnt(d, i, doc, zdi);
                }
            }

            _thetadk = estimateTheta(trainData, _thetadk, _ndk, _nds);
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
                    excludeTestCnt(d, i, testZdi);
                    tempZXdi = sampleZXdi(d, i, doc);
                    testZdi[d][i] = tempZXdi[1];
                    testXdi[d][i] = tempZXdi[0];
                    includeTestCnt(d, i, testZdi);
                }
            }

            _testThetadk = estimateTheta(testData, _testThetadk, _testNdk, _testNds);

            //compute log-likelihood
            logLikelihoodTrain.add(computeLogLikelihood(trainData, _thetadk));
            logLikelihoodTest.add(computeLogLikelihood(testData, _testThetadk));
            timeStamp[t-1] = (System.nanoTime() - startTime) / 1000000;
        }

        outputData(outputFile, thetadkSample, phikwSample, phickwSample, logLikelihoodTrain, logLikelihoodTest);
        outputTime(timeStamp, outputFile);
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

        TimedBlockCollapsedGibbs tbcg = new TimedBlockCollapsedGibbs();
        try {
            tbcg.sampling(trainFile, testFile, outputFile, k, lambda, alpha, beta, iterNum, biNum);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
