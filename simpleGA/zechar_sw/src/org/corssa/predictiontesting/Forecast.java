package org.corssa.predictiontesting;

import java.io.FileOutputStream;
import java.io.BufferedOutputStream;
import java.io.BufferedWriter;
import java.io.OutputStreamWriter;
import java.util.Locale;
import java.io.IOException;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

/**
 * @author J. Douglas Zechar zechar at usc.edu
 */
public class Forecast {

    private float[] alarmFunctionValues;
    private float numberOfForecastEvents = 0f;
    private float minDepth, maxDepth, depthDiscretization;
    private int numberOfDepthBoxes;
    private float minLat, maxLat, latDiscretization;
    private int numberOfLatBoxes;
    private float minLon, maxLon, lonDiscretization;
    private int numberOfLonBoxes;
    private float minMag, maxMag, magDiscretization;
    private int numberOfMagBoxes;
    private String ns0 = "http://www.scec.org/xml-ns/csep/forecast/0.1";
    private String publicID = "smi:org.scec/csep/forecast/1";
    private String modelName;
    private String version;
    private String author;
    private String issueDate;
    private String forecastStartDate;
    private String forecastEndDate;
    private String lastMagBinOpen;
    private Document dom;
    private int numberOfActiveBins = 0;

    public float numberOfForecastEvents() {
        return this.numberOfForecastEvents;
    }

    public String modelName() {
        return this.modelName;
    }

    public int numberOfBins() {
        return this.numberOfDepthBoxes * this.numberOfLatBoxes
                * this.numberOfLonBoxes * this.numberOfMagBoxes;
    }

    public int numberOfLatBoxes() {
        return this.numberOfLatBoxes;
    }

    public int numberOfActiveBins() {
        return this.numberOfActiveBins;
    }

    public int numberOfLonBoxes() {
        return this.numberOfLonBoxes;
    }

    public float[] values() {
        return this.alarmFunctionValues;
    }

    public float minLat() {
        return this.minLat;
    }

    public float maxLat() {
        return this.maxLat;
    }

    public float minLon() {
        return this.minLon;
    }

    public float maxLon() {
        return this.maxLon;
    }

    public float boxSize() {
        return this.latDiscretization;
    }

    public float minMag() {
        return this.minMag;
    }

    public float maxMag() {
        return this.maxMag;
    }

    public float magSpacing() {
        return this.magDiscretization;
    }

    /**
     * Creates a new instance of LatLonMagForecast
     */
    public Forecast() {
    }

    /**
     * Read the ForecastML file and instantiate the corresponding object.
     * The result is a grid with the forecasted seismicity rate in each grid box.
     *
     * @param forecastFile path to file containing alarm function values
     */
    public Forecast(String forecastMLFile, boolean useMaskBit) {
        //get the factory
        DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();

        try {
            //Using factory get an instance of document builder
            DocumentBuilder db = dbf.newDocumentBuilder();

            //parse using builder to get DOM representation of the XML file
            this.dom = db.parse(forecastMLFile);

            //get the root elememt
            Element docEle = dom.getDocumentElement();

            // get model meta-information
            Element forecastDataElement = (Element) docEle.getElementsByTagName("ns0:forecastData").item(0);
            if (forecastDataElement == null) {
                forecastDataElement = (Element) docEle.getElementsByTagName("forecastData").item(0);
            }
            this.publicID = forecastDataElement.getAttribute("publicID");

            Element modelNameElement = (Element) docEle.getElementsByTagName("ns0:modelName").item(0);
            if (modelNameElement == null) {
                modelNameElement = (Element) docEle.getElementsByTagName("modelName").item(0);
            }
            this.modelName = modelNameElement.getTextContent();

            Element versionElement = (Element) docEle.getElementsByTagName("ns0:version").item(0);
            if (versionElement == null) {
                versionElement = (Element) docEle.getElementsByTagName("version").item(0);
            }
            this.version = versionElement.getTextContent();

            Element authorElement = (Element) docEle.getElementsByTagName("ns0:author").item(0);
            if (authorElement == null) {
                authorElement = (Element) docEle.getElementsByTagName("author").item(0);
            }
            this.author = authorElement.getTextContent();

            Element issueDateElement = (Element) docEle.getElementsByTagName("ns0:issueDate").item(0);
            if (issueDateElement == null) {
                issueDateElement = (Element) docEle.getElementsByTagName("issueDate").item(0);
            }
            this.issueDate = issueDateElement.getTextContent();

            Element forecastStartDateElement = (Element) docEle.getElementsByTagName("ns0:forecastStartDate").item(0);
            if (forecastStartDateElement == null) {
                forecastStartDateElement = (Element) docEle.getElementsByTagName("forecastStartDate").item(0);
            }
            this.forecastStartDate = forecastStartDateElement.getTextContent();

            Element forecastEndDateElement = (Element) docEle.getElementsByTagName("ns0:forecastEndDate").item(0);
            if (forecastEndDateElement == null) {
                forecastEndDateElement = (Element) docEle.getElementsByTagName("forecastEndDate").item(0);
            }
            this.forecastEndDate = forecastEndDateElement.getTextContent();

            Element lastMagBinOpenElement = (Element) docEle.getElementsByTagName("ns0:lastMagBinOpen").item(0);
            if (lastMagBinOpenElement == null) {
                lastMagBinOpenElement = (Element) docEle.getElementsByTagName("lastMagBinOpen").item(0);
            }
            this.lastMagBinOpen = lastMagBinOpenElement.getTextContent();

            // get the cell dimension information
            Element cellDimension = (Element) docEle.getElementsByTagName("ns0:defaultCellDimension").item(0);
            if (cellDimension == null) {
                cellDimension = (Element) docEle.getElementsByTagName("defaultCellDimension").item(0);
            }
            this.latDiscretization =
                    Float.parseFloat(cellDimension.getAttribute("latRange"));
            this.lonDiscretization =
                    Float.parseFloat(cellDimension.getAttribute("lonRange"));

            Element magDiscretizationElement = (Element) docEle.getElementsByTagName("ns0:defaultMagBinDimension").item(0);
            if (magDiscretizationElement == null) {
                magDiscretizationElement = (Element) docEle.getElementsByTagName("defaultMagBinDimension").item(0);
            }
            this.magDiscretization =
                    Float.parseFloat(magDiscretizationElement.getTextContent());

            // get all depth layers and determine the min/max depth
            NodeList listOfDepthLayers =
                    docEle.getElementsByTagName("ns0:depthLayer");
            if (listOfDepthLayers.getLength() == 0) {
                listOfDepthLayers = docEle.getElementsByTagName("depthLayer");
            }
            int numberOfDepthSlices = listOfDepthLayers.getLength();
            float minDepthLocal = Float.MAX_VALUE;
            float maxDepthLocal = Float.MIN_VALUE;

            for (int i = 0; i < numberOfDepthSlices; i++) {
                Element depthLayer = (Element) listOfDepthLayers.item(i);
                float min = Float.parseFloat(depthLayer.getAttribute("min"));
                float max = Float.parseFloat(depthLayer.getAttribute("max"));
                this.depthDiscretization = max - min;
                if (min < minDepthLocal) {
                    minDepthLocal = min;
                }
                if (max > maxDepthLocal) {
                    maxDepthLocal = max;
                }
            }
            this.maxDepth = maxDepthLocal;
            this.minDepth = minDepthLocal;
            this.numberOfDepthBoxes = Math.round((this.maxDepth - this.minDepth)
                    / this.depthDiscretization);

            // get all cells, and determine the number of cells and the
            // total number of bins
            NodeList listOfCells = docEle.getElementsByTagName("ns0:cell");
            if (listOfCells.getLength() == 0) {
                listOfCells = docEle.getElementsByTagName("cell");
            }
            int numberOfCells = listOfCells.getLength();
            int numberOfBins = docEle.getElementsByTagName("ns0:bin").getLength();
            if (numberOfBins == 0) {
                numberOfBins = docEle.getElementsByTagName("bin").getLength();
            }
//            this.numberOfActiveBins = numberOfBins;

            // determine the min/max lat/lon
            float minLatLocal = 90f;
            float maxLatLocal = -90f;
            float minLonLocal = 180f;
            float maxLonLocal = -180f;

            for (int i = 0; i < numberOfCells; i++) {
                Element cell = (Element) listOfCells.item(i);
                float lat = Float.parseFloat(cell.getAttribute("lat"));
                if (lat < minLatLocal) {
                    minLatLocal = lat;
                }
                if (lat > maxLatLocal) {
                    maxLatLocal = lat;
                }
                float lon = Float.parseFloat(cell.getAttribute("lon"));
                if (lon > 180f) {
                    lon -= 360f;
                }
                if (lon < minLonLocal) {
                    minLonLocal = lon;
                }
                if (lon > maxLonLocal) {
                    maxLonLocal = lon;
                }
            }

            Element firstCell = (Element) listOfCells.item(0);
            NodeList firstCellBins = firstCell.getElementsByTagName("ns0:bin");
            if (firstCellBins.getLength() == 0) {
                firstCellBins = firstCell.getElementsByTagName("bin");
            }
            int numberOfBinsPerCell = numberOfBins / numberOfCells;

            // Determine the min/max depth boundaries
            float minMagLocal = Float.MAX_VALUE;
            float maxMagLocal = Float.MIN_VALUE;

            for (int i = 0; i < numberOfBinsPerCell; i++) {
                Element bin = (Element) firstCellBins.item(i);
                float mag = Float.parseFloat(bin.getAttribute("m"));
                if (mag < minMagLocal) {
                    minMagLocal = mag;
                }
                if (mag > maxMagLocal) {
                    maxMagLocal = mag;
                }
            }

            this.minLat = minLatLocal - 0.5f * this.latDiscretization;
            this.maxLat = maxLatLocal + 0.5f * this.latDiscretization;
            this.minLon = minLonLocal - 0.5f * this.lonDiscretization;
            this.maxLon = maxLonLocal + 0.5f * this.lonDiscretization;
            this.minMag = minMagLocal - 0.5f * this.magDiscretization;
            this.maxMag = maxMagLocal + 0.5f * this.magDiscretization;

            this.numberOfLatBoxes = Math.round((this.maxLat - this.minLat)
                    / this.latDiscretization);
            this.numberOfLonBoxes = Math.round((this.maxLon - this.minLon)
                    / this.lonDiscretization);
            this.numberOfMagBoxes = Math.round((this.maxMag - this.minMag)
                    / this.magDiscretization);

            // initialize the alarm function vector to the appropriate size
            this.alarmFunctionValues = new float[this.numberOfDepthBoxes
                    * this.numberOfLatBoxes * this.numberOfLonBoxes
                    * this.numberOfMagBoxes];
            for (int i = 0; i < alarmFunctionValues.length; i++) {
                this.alarmFunctionValues[i] = Float.NEGATIVE_INFINITY;
            }

            for (int k = 0; k < numberOfDepthSlices; k++) {
                Element depthLayer = (Element) listOfDepthLayers.item(k);
                float depth = Float.parseFloat(depthLayer.getAttribute("min"));
                for (int i = 0; i < numberOfCells; i++) {
                    Element cell = (Element) listOfCells.item(i);
                    String maskAttr = cell.getAttribute("mask").trim();
                    int maskBit = 1;
                    if (maskAttr.length() > 0) {
                        maskBit = Integer.parseInt(maskAttr.trim());
                    }
                    if (!useMaskBit || maskBit == 1) {
                        float lat = MathUtil.roundedToNearest(
                                Float.parseFloat(cell.getAttribute("lat"))
                                - 0.5f * this.latDiscretization, 0.5f
                                * this.latDiscretization);
                        float lon = MathUtil.roundedToNearest(
                                Float.parseFloat(cell.getAttribute("lon"))
                                - 0.5f * this.latDiscretization, 0.5f
                                * this.latDiscretization);
                        if (lon > 180f) {
                            lon -= 360f;
                        }

                        NodeList cellBins =
                                cell.getElementsByTagName("ns0:bin");
                        if (cellBins.getLength() == 0) {
                            cellBins = cell.getElementsByTagName("bin");
                        }
                        for (int j = 0; j < numberOfBinsPerCell; j++) {
                            Element bin = (Element) cellBins.item(j);
                            float mag = MathUtil.roundedToNearest(
                                    Float.parseFloat(bin.getAttribute("m"))
                                    - 0.5f * this.magDiscretization, 0.5f
                                    * this.magDiscretization);
                            // float mag = Float.parseFloat(bin.getAttribute("m"))  - 0.5f * this.sizeOfMagCell;
                            float forecastRate = Float.parseFloat(bin.getTextContent());

                            int voxel = ArrayUtil.voxelToWhichValueBelongs(this.minDepth, this.maxDepth, this.minLat, this.maxLat, this.minLon, this.maxLon, this.minMag, this.maxMag,
                                    this.depthDiscretization, this.latDiscretization, this.lonDiscretization, this.magDiscretization, depth, lat, lon, mag);
                            // System.out.println("(voxel, value) = (" + voxel + ", " + forecastRate + ")");
                            // translate the 4D cell position to the corresponding vector position
                            //int boxPosition = ArrayUtil.boxToWhichValueBelongs(this.minLon, this.maxLon, this.minLat, this.maxLat,
//                                this.minMag, this.maxMag, this.latDiscretization, this.latDiscretization, this.magDiscretization, lon, lat, mag);
//
//                        if (boxPosition >= this.alarmFunctionValues.length) {
//                            System.err.println("Error in determining cell position from lat/lon!");
//                            System.exit(-1);
//                        }

                            // set the alarm function value in the appropriate vector position
                            this.alarmFunctionValues[voxel] = forecastRate;
                            this.numberOfForecastEvents += forecastRate;
                            this.numberOfActiveBins++;
                        }
                    }
                }

            }
        } catch (ParserConfigurationException pce) {
            pce.printStackTrace();
        } catch (SAXException se) {
            se.printStackTrace();
        } catch (IOException ioe) {
            ioe.printStackTrace();
        }
    }

    /**
     * Read the ForecastML file and instantiate the corresponding object.  The result is a grid with the forecasted seismicity rate in each grid box.  We then filter the
     * forecast values according to the filter, so that only values in those bins allowed by the filter are allowed.
     *
     * @param forecastFile path to file containing alarm function values
     * @param filter boolean filter matrix that determines which forecast bins may have a positive forecast value
     */
    public Forecast(String forecastMLFile, boolean[] filter) {
        //get the factory
        DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();

        try {
            //Using factory get an instance of document builder
            DocumentBuilder db = dbf.newDocumentBuilder();

            //parse using builder to get DOM representation of the XML file
            this.dom = db.parse(forecastMLFile);

            //get the root elememt
            Element docEle = dom.getDocumentElement();

            // get model meta-information
            //Element topLevelElement = (Element) docEle.getElementsByTagName("ns0:CSEPForecast").item(0);
            //this.ns0 = topLevelElement.getAttribute("xml:ns0");
            Element forecastDataElement = (Element) docEle.getElementsByTagName("ns0:forecastData").item(0);
            if (forecastDataElement == null) {
                forecastDataElement = (Element) docEle.getElementsByTagName("forecastData").item(0);
            }
            this.publicID = forecastDataElement.getAttribute("publicID");

            Element modelNameElement = (Element) docEle.getElementsByTagName("ns0:modelName").item(0);
            if (modelNameElement == null) {
                modelNameElement = (Element) docEle.getElementsByTagName("modelName").item(0);
            }
            this.modelName = modelNameElement.getTextContent();

            Element versionElement = (Element) docEle.getElementsByTagName("ns0:version").item(0);
            if (versionElement == null) {
                versionElement = (Element) docEle.getElementsByTagName("version").item(0);
            }
            this.version = versionElement.getTextContent();

            Element authorElement = (Element) docEle.getElementsByTagName("ns0:author").item(0);
            if (authorElement == null) {
                authorElement = (Element) docEle.getElementsByTagName("author").item(0);
            }
            this.author = authorElement.getTextContent();

            Element issueDateElement = (Element) docEle.getElementsByTagName("ns0:issueDate").item(0);
            if (issueDateElement == null) {
                issueDateElement = (Element) docEle.getElementsByTagName("issueDate").item(0);
            }
            this.issueDate = issueDateElement.getTextContent();

            Element forecastStartDateElement = (Element) docEle.getElementsByTagName("ns0:forecastStartDate").item(0);
            if (forecastStartDateElement == null) {
                forecastStartDateElement = (Element) docEle.getElementsByTagName("forecastStartDate").item(0);
            }
            this.forecastStartDate = forecastStartDateElement.getTextContent();

            Element forecastEndDateElement = (Element) docEle.getElementsByTagName("ns0:forecastEndDate").item(0);
            if (forecastEndDateElement == null) {
                forecastEndDateElement = (Element) docEle.getElementsByTagName("forecastEndDate").item(0);
            }
            this.forecastEndDate = forecastEndDateElement.getTextContent();

            Element lastMagBinOpenElement = (Element) docEle.getElementsByTagName("ns0:lastMagBinOpen").item(0);
            if (lastMagBinOpenElement == null) {
                lastMagBinOpenElement = (Element) docEle.getElementsByTagName("lastMagBinOpen").item(0);
            }
            this.lastMagBinOpen = lastMagBinOpenElement.getTextContent();

            // get the cell dimension information
            Element cellDimension = (Element) docEle.getElementsByTagName("ns0:defaultCellDimension").item(0);
            if (cellDimension == null) {
                cellDimension = (Element) docEle.getElementsByTagName("defaultCellDimension").item(0);
            }
            this.latDiscretization = Float.parseFloat(cellDimension.getAttribute("latRange"));
            this.lonDiscretization = Float.parseFloat(cellDimension.getAttribute("lonRange"));

            Element magDiscretizationElement = (Element) docEle.getElementsByTagName("ns0:defaultMagBinDimension").item(0);
            if (magDiscretizationElement == null) {
                magDiscretizationElement = (Element) docEle.getElementsByTagName("defaultMagBinDimension").item(0);
            }
            this.magDiscretization = Float.parseFloat(magDiscretizationElement.getTextContent());

            // get all depth layers and determine the min/max depth
            NodeList listOfDepthLayers = docEle.getElementsByTagName("ns0:depthLayer");
            if (listOfDepthLayers.getLength() == 0) {
                listOfDepthLayers = docEle.getElementsByTagName("depthLayer");
            }
            int numberOfDepthSlices = listOfDepthLayers.getLength();
            float minDepthLocal = Float.MAX_VALUE;
            float maxDepthLocal = Float.MIN_VALUE;

            for (int i = 0; i < numberOfDepthSlices; i++) {
                Element depthLayer = (Element) listOfDepthLayers.item(i);
                float min = Float.parseFloat(depthLayer.getAttribute("min"));
                float max = Float.parseFloat(depthLayer.getAttribute("max"));
                this.depthDiscretization = max - min;
                if (min < minDepthLocal) {
                    minDepthLocal = min;
                }
                if (max > maxDepthLocal) {
                    maxDepthLocal = max;
                }
            }
            this.maxDepth = maxDepthLocal;
            this.minDepth = minDepthLocal;
            this.numberOfDepthBoxes = Math.round((this.maxDepth - this.minDepth) / this.depthDiscretization);

            // get all cells, and determine the number of cells and the total number of bins
            NodeList listOfCells = docEle.getElementsByTagName("ns0:cell");
            if (listOfCells.getLength() == 0) {
                listOfCells = docEle.getElementsByTagName("cell");
            }
            int numberOfCells = listOfCells.getLength();
            int numberOfBins = docEle.getElementsByTagName("ns0:bin").getLength();
            if (numberOfBins == 0) {
                numberOfBins = docEle.getElementsByTagName("bin").getLength();
            }
//            this.numberOfActiveBins = numberOfBins;

            // determine the min/max lat/lon
            float minLatLocal = 90f;
            float maxLatLocal = -90f;
            float minLonLocal = 180f;
            float maxLonLocal = -180f;

            for (int i = 0; i < numberOfCells; i++) {
                Element cell = (Element) listOfCells.item(i);
                float lat = Float.parseFloat(cell.getAttribute("lat"));
                if (lat < minLatLocal) {
                    minLatLocal = lat;
                }
                if (lat > maxLatLocal) {
                    maxLatLocal = lat;
                }
                float lon = Float.parseFloat(cell.getAttribute("lon"));
                if (lon > 180f) {
                    lon -= 360f;
                }
                if (lon < minLonLocal) {
                    minLonLocal = lon;
                }
                if (lon > maxLonLocal) {
                    maxLonLocal = lon;
                }
            }

            Element firstCell = (Element) listOfCells.item(0);
            NodeList firstCellBins = firstCell.getElementsByTagName("ns0:bin");
            if (firstCellBins.getLength() == 0) {
                firstCellBins = firstCell.getElementsByTagName("bin");
            }
            int numberOfBinsPerCell = numberOfBins / numberOfCells;

            // Determine the min/max depth boundaries
            float minMagLocal = Float.MAX_VALUE;
            float maxMagLocal = Float.MIN_VALUE;

            for (int i = 0; i < numberOfBinsPerCell; i++) {
                Element bin = (Element) firstCellBins.item(i);
                float mag = Float.parseFloat(bin.getAttribute("m"));
                if (mag < minMagLocal) {
                    minMagLocal = mag;
                }
                if (mag > maxMagLocal) {
                    maxMagLocal = mag;
                }
            }

            this.minLat = minLatLocal - 0.5f * this.latDiscretization;
            this.maxLat = maxLatLocal + 0.5f * this.latDiscretization;
            this.minLon = minLonLocal - 0.5f * this.lonDiscretization;
            this.maxLon = maxLonLocal + 0.5f * this.lonDiscretization;
            this.minMag = minMagLocal - 0.5f * this.magDiscretization;
            this.maxMag = maxMagLocal + 0.5f * this.magDiscretization;

//            System.out.println("for " + forecastMLFile);
//            System.out.println("min (lat, lon, mag, depth) = (" + minLatLocal + ", " + minLonLocal + ", " + minMagLocal + ", " + minDepthLocal + ")");
//            System.out.println("max (lat, lon, mag, depth) = (" + maxLatLocal + ", " + maxLonLocal + ", " + maxMagLocal + ", " + maxDepthLocal + ")");

            this.numberOfLatBoxes = Math.round((this.maxLat - this.minLat) / this.latDiscretization);
            this.numberOfLonBoxes = Math.round((this.maxLon - this.minLon) / this.lonDiscretization);
            this.numberOfMagBoxes = Math.round((this.maxMag - this.minMag) / this.magDiscretization);

            // initialize the alarm function vector to the appropriate size
            this.alarmFunctionValues = new float[this.numberOfDepthBoxes * this.numberOfLatBoxes * this.numberOfLonBoxes * this.numberOfMagBoxes];
            for (int i = 0; i < alarmFunctionValues.length; i++) {
                this.alarmFunctionValues[i] = Float.NEGATIVE_INFINITY;
            }

            for (int k = 0; k < numberOfDepthSlices; k++) {
                Element depthLayer = (Element) listOfDepthLayers.item(k);
                float depth = Float.parseFloat(depthLayer.getAttribute("min"));
                for (int i = 0; i < numberOfCells; i++) {
                    Element cell = (Element) listOfCells.item(i);
                    float lat = MathUtil.roundedToNearest(Float.parseFloat(cell.getAttribute("lat")) - 0.5f * this.latDiscretization, 0.5f * this.latDiscretization);
                    float lon = MathUtil.roundedToNearest(Float.parseFloat(cell.getAttribute("lon")) - 0.5f * this.latDiscretization, 0.5f * this.latDiscretization);
                    if (lon > 180f) {
                        lon -= 360f;
                    }
                    NodeList cellBins = cell.getElementsByTagName("ns0:bin");
                    if (cellBins.getLength() == 0) {
                        cellBins = cell.getElementsByTagName("bin");
                    }
                    for (int j = 0; j < numberOfBinsPerCell; j++) {
                        Element bin = (Element) cellBins.item(j);
                        float mag = MathUtil.roundedToNearest(Float.parseFloat(bin.getAttribute("m")) - 0.5f * this.magDiscretization, 0.5f * this.magDiscretization);
                        // float mag = Float.parseFloat(bin.getAttribute("m"))  - 0.5f * this.sizeOfMagCell;
                        float forecastRate = Float.parseFloat(bin.getTextContent());

                        int voxel = ArrayUtil.voxelToWhichValueBelongs(this.minDepth, this.maxDepth, this.minLat, this.maxLat, this.minLon, this.maxLon, this.minMag, this.maxMag,
                                this.depthDiscretization, this.latDiscretization, this.lonDiscretization, this.magDiscretization, depth, lat, lon, mag);
                        // System.out.println("(voxel, value) = (" + voxel + ", " + forecastRate + ")");
                        // translate the 4D cell position to the corresponding vector position
                        //int boxPosition = ArrayUtil.boxToWhichValueBelongs(this.minLon, this.maxLon, this.minLat, this.maxLat,
//                                this.minMag, this.maxMag, this.latDiscretization, this.latDiscretization, this.magDiscretization, lon, lat, mag);
//
//                        if (boxPosition >= this.alarmFunctionValues.length) {
//                            System.err.println("Error in determining cell position from lat/lon!");
//                            System.exit(-1);
//                        }

                        // set the alarm function value in the appropriate vector position, if the filter allows it
                        if (filter[voxel]) {
//                            System.out.println(lon + "\t" + lat + "\t" + mag);
                            this.alarmFunctionValues[voxel] = forecastRate;
                            this.numberOfForecastEvents += forecastRate;
                            this.numberOfActiveBins++;
                        }
                    }
                }

            }
        } catch (ParserConfigurationException pce) {
            pce.printStackTrace();
        } catch (SAXException se) {
            se.printStackTrace();
        } catch (IOException ioe) {
            ioe.printStackTrace();
        }
    }

    /**
     * Save the current forecast values and parameters in ForecastML format
     *
     * @param outputFile path to ForecastML file
     */
    public void saveForecastML(String outputFile) {
        try {
            FileOutputStream oOutFIS = new FileOutputStream(outputFile);
            BufferedOutputStream oOutBIS = new BufferedOutputStream(oOutFIS);
            BufferedWriter oWriter = new BufferedWriter(new OutputStreamWriter(oOutBIS));

            Locale us = new Locale("en", "us");
            oWriter.write("<ns0:CSEPForecast xmlns:ns0=\"" + this.ns0 + "\">\n");
            oWriter.write("  <ns0:forecastData publicID=\"" + this.publicID + "\">\n");
            oWriter.write("    <ns0:modelName>" + this.modelName + "</ns0:modelName>\n");
            oWriter.write("    <ns0:version>" + this.version + "</ns0:version>\n");
            oWriter.write("    <ns0:author>" + this.author + "</ns0:author>\n");
            oWriter.write("    <ns0:issueDate>" + this.issueDate + "</ns0:issueDate>\n");
            oWriter.write("    <ns0:forecastStartDate>" + this.forecastStartDate + "</ns0:forecastStartDate>\n");
            oWriter.write("    <ns0:forecastEndDate>" + this.forecastEndDate + "</ns0:forecastEndDate>\n");
            oWriter.write("    <ns0:defaultCellDimension latRange=\"" + this.latDiscretization + "\" lonRange=\"" + this.lonDiscretization + "\" />\n");
            oWriter.write("    <ns0:defaultMagBinDimension>" + this.magDiscretization + "</ns0:defaultMagBinDimension>\n");
            oWriter.write("    <ns0:lastMagBinOpen>" + this.lastMagBinOpen + "</ns0:lastMagBinOpen>\n");
            for (int i = 0; i < this.numberOfDepthBoxes; i++) {
                float depthLayerMin = this.minDepth + i * this.depthDiscretization;
                float depthLayerMax = depthLayerMin + this.depthDiscretization;
                oWriter.write("    <ns0:depthLayer max=\"" + depthLayerMax + "\" min=\"" + depthLayerMin + "\">\n");
                for (int j = 0; j < this.numberOfLatBoxes; j++) {
                    float lat = this.minLat + j * this.latDiscretization + 0.5f * this.latDiscretization;
                    for (int k = 0; k < this.numberOfLonBoxes; k++) {
                        float lon = this.minLon + k * this.lonDiscretization + 0.5f * this.lonDiscretization;
                        if (this.isPartOfForecast(i, j, k)) {
                            oWriter.write("      <ns0:cell lat=\"" + lat + "\" lon=\"" + lon + "\" mask=\"1\">\n");
                            for (int l = 0; l < this.numberOfMagBoxes; l++) {
                                float mag = this.minMag + l * this.magDiscretization + 0.5f * this.magDiscretization;
                                int voxel = i * this.numberOfLatBoxes * this.numberOfLonBoxes * this.numberOfMagBoxes + j * this.numberOfLonBoxes * this.numberOfMagBoxes + k * this.numberOfMagBoxes + l;
                                float forecastValue = this.alarmFunctionValues[voxel];
                                if (forecastValue > Float.MIN_VALUE) {
                                    oWriter.write("        <ns0:bin m=\"" + mag + "\">" + forecastValue + "</ns0:bin>\n");
                                }
                            }
                            oWriter.write("      </ns0:cell>\n");
                        }
                    }
                }
                oWriter.write("    </ns0:depthLayer>\n");
            }
            oWriter.write("  </ns0:forecastData>\n");
            oWriter.write("</ns0:CSEPForecast>");

            oWriter.close();
            oOutBIS.close();
            oOutFIS.close();

        } catch (Exception ex) {
            System.out.println("Error in Forecast.saveForecastML(" + outputFile + ")");
            ex.printStackTrace();
        }

    }

    /**
     * Determine if the specified depth/lat/lon cell is active.  To do this, we check all of its constituent magnitude bins to see if any has a forecast rate greater than
     * Float.NEGATIVE_INFINITY.
     * 
     * @param depthLayer depth layer of interest
     * @param lat latitude index of interest
     * @param lon longitude index of interest
     * @return boolean response to the question: Is the given depth/lat/lon space part of this forecast?
     */
    public boolean isPartOfForecast(int depthLayer, int latIndex, int lonIndex) {
        boolean isActive = false;
        for (int i = 0; i < this.numberOfMagBoxes; i++) {
            int voxel = depthLayer * this.numberOfLatBoxes * this.numberOfLonBoxes * this.numberOfMagBoxes + latIndex * this.numberOfLonBoxes * this.numberOfMagBoxes + lonIndex * this.numberOfMagBoxes + i;
            if (this.alarmFunctionValues[voxel] > Float.NEGATIVE_INFINITY) {
                return true;
            }
        }
        return isActive;
    }

    /**
     * Determine if the specified voxel cell is active.  To do this, we check to see if it has a forecast rate greater than Float.NEGATIVE_INFINITY.
     * 
     * @param voxel voxel of interest
     * @return boolean response to the question: Is the given depth/lat/lon/mag bin part of this forecast?
     */
    public boolean isPartOfForecast(int voxel) {
        boolean isActive = false;
        if (this.alarmFunctionValues[voxel] > Float.NEGATIVE_INFINITY) {
            return true;
        }
        return isActive;
    }

    /**
     * Bin the specified target eqk catalog into the bins used by the current Forecast.  The result is an array with the number of epicenters occurring in each bin.
     *
     * @param catalogOfInterest eqk catalog to bin
     * @return array representing the forecast grid with each entry denoting the number of epicenters occuring in the bin
     */
    public short[] binnedCatalog(Catalog catalogOfInterest) {
        short[] eventMap = new short[this.alarmFunctionValues.length];

        int numberOfEqks = catalogOfInterest.numberOfEqks();
        float[] lats = catalogOfInterest.lats();
        float[] lons = catalogOfInterest.lons();
        float[] depths = catalogOfInterest.depths();
        float[] mags = catalogOfInterest.mags();

        for (int i = 0; i < numberOfEqks; i++) {
            int voxel = ArrayUtil.voxelToWhichValueBelongs(this.minDepth, this.maxDepth, this.minLat, this.maxLat, this.minLon, this.maxLon, this.minMag, this.maxMag, this.depthDiscretization,
                    this.latDiscretization, this.lonDiscretization, this.magDiscretization, depths[i], lats[i], lons[i], mags[i]);
//            System.out.println("eqk in voxel " + voxel);

            // check to make sure this event is in the study region; if the forecast rate here was not set when the forecast was instantiated, it will still be Float.NEGATIVE_INFINITY,
            // indicating that the current forecast does not cover the bin where the current eqk occurs
            float forecastRateHere = this.alarmFunctionValues[voxel];
//            if (forecastRateHere > Float.NEGATIVE_INFINITY) {
//                System.out.print(forecastRateHere + "\t");
//            } else {
//                System.out.print("n/a\t");
//            }
//            System.out.println("forecast rate in " + voxel + ": " + forecastRateHere);
            if (forecastRateHere > Float.NEGATIVE_INFINITY && voxel > -1) {
                // add this event in the appropriate box
                eventMap[voxel]++;
            } else {
//                System.err.println("It appears that the event at (depth, lat, lon, mag) = (" + depths[i] + ", " + lats[i] + ", " + lons[i] + ", " + mags[i] + ") " +
//                        "falls in a bin that is not part of this forecast.");
            }
        }
//        System.out.println("");
        return eventMap;
    }

    /**
     * Bin the specified target eqk catalog into the spatial bins used by the current Forecast.  The result is an array with the number of epicenters occurring in each spatial cell.
     *
     * @param catalogOfInterest eqk catalog to bin
     * @return array representing the forecast grid with each entry denoting the number of epicenters occuring in the bin
     */
    public short[] binnedMagnitudeCatalog(Catalog catalogOfInterest) {
        short[] eventMap = this.binnedCatalog(catalogOfInterest);
        short[] magnitudeEventMap = new short[this.numberOfMagBoxes];

        for (int voxel = 0; voxel < eventMap.length; voxel++) {
            if (eventMap[voxel] > 0) {
                // map the voxel to the appropriate spatial bin
                int[] indices =
                        ArrayUtil.arrayIndicesCorrespondingToVoxel(this.minDepth, this.maxDepth, this.minLat,
                        this.maxLat, this.minLon, this.maxLon, this.minMag, this.maxMag, this.depthDiscretization,
                        this.latDiscretization, this.lonDiscretization, this.magDiscretization, voxel);
                int magBin = indices[0];
                magnitudeEventMap[magBin] += eventMap[voxel];
            }
        }
        return magnitudeEventMap;
    }

    /**
     * Bin the specified target eqk catalog into the spatial bins used by the current Forecast.  The result is an array with the number of epicenters occurring in each spatial cell.
     *
     * @param catalogOfInterest eqk catalog to bin
     * @return array representing the forecast grid with each entry denoting the number of epicenters occuring in the bin
     */
    public short[] binnedSpatialCatalog(Catalog catalogOfInterest) {
        short[] eventMap = this.binnedCatalog(catalogOfInterest);
        short[] spatialEventMap = new short[this.numberOfLatBoxes * this.numberOfLonBoxes];

        for (int voxel = 0; voxel < eventMap.length; voxel++) {
            // map the voxel to the appropriate spatial bin
            int[] indices =
                    ArrayUtil.arrayIndicesCorrespondingToVoxel(this.minDepth, this.maxDepth, this.minLat,
                    this.maxLat, this.minLon, this.maxLon, this.minMag, this.maxMag, this.depthDiscretization,
                    this.latDiscretization, this.lonDiscretization, this.magDiscretization, voxel);
            int latBin = indices[2];
            int lonBin = indices[1];
            int spaceBin = latBin * this.numberOfLonBoxes + lonBin;
            spatialEventMap[spaceBin] += eventMap[voxel];
        }
        return spatialEventMap;
    }

    /**
     * Set the values for this forecast to the specified values
     */
//    public void setForecastValues(float[] forecast){
//        this.numberOfActiveBins = 0;
//        
//        // copy the forecast values, and count the number of active bins (those bins w/ forecast value greater than -Infinity)
//        for (int i = 0;i < forecast.length;i++){
//            float forecastValue = forecast[i];
//            this.alarmFunctionValues[i] = forecastValue;
//            if (forecastValue > Float.NEGATIVE_INFINITY){
//                this.numberOfActiveBins++;
//            }
//        }
//    }
    /**
     * Generate a reduced forecast that only contains the magnitude component of the original
     * space-rate-magnitude forecast.
     */
    public float[] magnitudeForecast() {
        float[] magnitudeForecast = new float[this.numberOfMagBoxes];

        for (int voxel = 0; voxel < this.alarmFunctionValues.length; voxel++) {
            // map the voxel to the appropriate magnitude bin
            if (!Float.isInfinite(this.alarmFunctionValues[voxel])) {
                int[] indices =
                        ArrayUtil.arrayIndicesCorrespondingToVoxel(this.minDepth, this.maxDepth, this.minLat,
                        this.maxLat, this.minLon, this.maxLon, this.minMag, this.maxMag, this.depthDiscretization,
                        this.latDiscretization, this.lonDiscretization, this.magDiscretization, voxel);
                int magBin = indices[0];
                magnitudeForecast[magBin] += this.alarmFunctionValues[voxel];
            }
        }
        magnitudeForecast = ArrayUtil.normalize(magnitudeForecast);
        return magnitudeForecast;
    }

    /**
     * Generate a reduced forecast that only contains the spatial component of the original
     * space-rate-magnitude forecast.
     */
    public float[] spatialForecast() {
        float[] spatialForecast = new float[this.numberOfLatBoxes
                * this.numberOfLonBoxes];

        for (int voxel = 0; voxel < this.alarmFunctionValues.length; voxel++) {
            // map the voxel to the appropriate spatial bin
            if (!Float.isInfinite(this.alarmFunctionValues[voxel])) {
                int[] indices =
                        ArrayUtil.arrayIndicesCorrespondingToVoxel(this.minDepth, this.maxDepth, this.minLat,
                        this.maxLat, this.minLon, this.maxLon, this.minMag, this.maxMag, this.depthDiscretization,
                        this.latDiscretization, this.lonDiscretization, this.magDiscretization, voxel);
                int latBin = indices[2];
                int lonBin = indices[1];
                int spaceBin = latBin * this.numberOfLonBoxes + lonBin;

//                if (spaceBin == 82) {
//                    System.out.println("here's a problem!");
//                    int magBin = indices[0];
//                    int depthBin = indices[3];
//                    float latValue = minLat + latBin * latDiscretization;
//                    float lonValue = minLon + lonBin * lonDiscretization;
//                    float magValue = minMag + magBin * magDiscretization;
//                    float depthValue = minDepth + depthBin * depthDiscretization;
//                    System.out.println("(depth, lat, lon, mag, rate) = (" + depthValue + ", " + latValue + ", " + lonValue + ", " + magValue + ", " + this.alarmFunctionValues[voxel] + ")");
//                }
                spatialForecast[spaceBin] += this.alarmFunctionValues[voxel];
            }
        }

//        for (int i = 0; i < spatialForecast.length; i++) {
//            if (spatialForecast[i] > 0) {
//                float[] latLon = ArrayUtil.arrayIndicesCorrespondingToCell(minLon, maxLon, minLat, maxLat, lonDiscretization, latDiscretization, i);
//                System.out.println("(lat, lon, rate) = (" + latLon[0] + ", " + latLon[1] + ", " + spatialForecast[i] + ")");
//            }
//        }
        spatialForecast = ArrayUtil.normalize(spatialForecast);
        return spatialForecast;
    }
}
