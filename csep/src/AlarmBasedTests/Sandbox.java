import java.util.Properties;
import java.io.InputStreamReader;
import java.io.BufferedInputStream;
import java.io.FileInputStream;
import java.io.BufferedReader;

public class Sandbox {

    /** Creates a new instance of Sandbox */
    public Sandbox() {
    }

    public static void main(String[] args) {
        if (args.length == 0) {
            System.err.println("Usage: Sandbox \"configurationFile\"");
            System.exit(-1);
        }

        String configurationFile = args[0];

        String pathToForecastFile = "";
        String[] pathsToOtherForecasts = null;
        String pathToCatalogFile = "";
        String pathToResultsFile = "";
        float alpha = 0f;
        long seed = 0L;
        boolean produceMatlabResults = false;
        boolean useMaskBit = false;
        String pathToSeedFile = "";

        try {
            FileInputStream oFIS = new FileInputStream(configurationFile);
            BufferedInputStream oBIS = new BufferedInputStream(oFIS);
            BufferedReader oReader = new BufferedReader(new InputStreamReader(oBIS));

            Properties props = new Properties();
            props.load(oFIS);
            oReader.close();
            oBIS.close();
            oFIS.close();

            // Set the properties from the configuration file
            pathToForecastFile = props.getProperty("pathToForecastFile");
            String listOfPathsToOtherForecasts = props.getProperty("pathsToOtherForecasts");
            if (listOfPathsToOtherForecasts != null) {
                pathsToOtherForecasts = listOfPathsToOtherForecasts.split(",");
            }
            pathToCatalogFile = props.getProperty("pathToCatalogFile");
            pathToResultsFile = props.getProperty("pathToResultsFile");
            alpha = Float.parseFloat(props.getProperty("alpha"));
            produceMatlabResults = Boolean.parseBoolean(props.getProperty("produceMatlabResults"));
            useMaskBit = Boolean.parseBoolean(props.getProperty("useMaskBit"));
            pathToSeedFile = props.getProperty("pathToSeedFile");

            oFIS = new FileInputStream(pathToSeedFile);
            oBIS = new BufferedInputStream(oFIS);
            oReader = new BufferedReader(new InputStreamReader(oBIS));

            props = new Properties();
            props.load(oFIS);
            oReader.close();
            oBIS.close();
            oFIS.close();
            seed = Long.parseLong(props.getProperty("seed"));
        } catch (Exception ex) {
            System.err.println("Error in reading configuration file or seed file.");
            ex.printStackTrace();
            System.exit(-1);
        }

        if (pathsToOtherForecasts == null) { // ROC computation
            Sandbox.rocComputation(pathToForecastFile, pathToCatalogFile, pathToResultsFile, alpha, seed, produceMatlabResults, useMaskBit);
        } else {
            Sandbox.molchanASSComputation(pathToForecastFile, pathsToOtherForecasts, pathToCatalogFile, pathToResultsFile, alpha, seed, produceMatlabResults, useMaskBit);
        }
    }

    /**
     * Perform an ROC computation (results in Matlab and XML format)
     */
    public static void rocComputation(String forecastFile, String catalogFile, String xmlFile, float alpha, long seed, boolean saveResultsInMatlab, boolean useMaskBit) {
        // Instantiate the rate forecast of interest from ForecastML file
        System.out.println("Instantiate the rate forecast of interest from ForecastML file");
        CSEPForecast forecast = new CSEPForecast(forecastFile, useMaskBit);

        // Instantiate a catalog of observed eqks from a ZMAP file
        System.out.println("Instantiate a catalog of observed eqks from a ZMAP file");
        Catalog catalog = new Catalog(catalogFile, Catalog.CSEP_ZMAP);

        // Compute ROC and confidence bounds for the given forecast and catalog, and save in Matlab and then XML format
        System.out.println("Compute ROC and confidence bounds for the given forecast and catalog, and save");
        ROCTools.roc(forecast, catalog, xmlFile, alpha, seed, saveResultsInMatlab);
    }

    /**
     * Perform a Molchan/ASS computation (results in Matlab and XML format)
     */
    public static void molchanASSComputation(String forecastFile, String[] otherForecastFiles, String catalogFile, String xmlFile, float alpha,
            long seed, boolean saveResultsInMatlab, boolean useMaskBit) {
        // Instantiate the reference rate forecast of interest from ForecastML file
//        System.out.println("Instantiate the reference rate forecast of interest from ForecastML file");
//        CSEPForecast referenceForecast = new CSEPForecast(forecastFile, useMaskBit);

        // Instantiate the rate forecasts that we wish to compare to the reference forecast
//        System.out.println("Instantiate the rate forecasts that we wish to compare to the reference forecast");
//        CSEPForecast[] forecasts = new CSEPForecast[otherForecastFiles.length];
//        for (int i = 0; i < forecasts.length; i++) {
//            forecasts[i] = new CSEPForecast(otherForecastFiles[i]);
//        }

        // Instantiate a catalog of observed eqks from a ZMAP file
        System.out.println("Instantiate a catalog of observed eqks from a ZMAP file");
        Catalog catalog = new Catalog(catalogFile, Catalog.CSEP_ZMAP);

        // Compute Molchan/ASS and confidence bounds for the given forecast and catalog, and save in Matlab and then XML format
        System.out.println("Compute Molchan/ASS and confidence bounds for the given forecast and catalog, and save");
        MolchanTools.molchanAndASS(forecastFile, otherForecastFiles, catalog, xmlFile, alpha, seed, saveResultsInMatlab, useMaskBit);
    }
}
