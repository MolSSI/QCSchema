package org.jmol.adapter.writers;

import java.io.OutputStream;
import java.util.Date;
import java.util.Hashtable;
import java.util.Map;

import javajs.util.DF;
import javajs.util.Lst;
import javajs.util.P3;
import javajs.util.PT;
import javajs.util.SB;

import org.jmol.api.SymmetryInterface;
import org.jmol.java.BS;
import org.jmol.modelset.Atom;
import org.jmol.quantum.SlaterData;
import org.jmol.util.JSONWriter;
import org.jmol.util.Vibration;
import org.jmol.viewer.Viewer;
import org.qcschema.QCSchemaUnits;

/**
 * A very experimental class for writing QCJSON files. This standard is in the
 * process of being developed, so any of this could change at any time.
 * 
 * All we have here is Bob Hanson's experiment with getting Jmol to save and
 * restore structures, vibrations, and molecular orbitals.
 * 
 * Data set Bob is using is at
 * 
 * https://sourceforge.net/p/jmol/code/HEAD/tree/trunk/Jmol-datafiles/qcjson
 * 
 */
public class QCJSONWriter extends JSONWriter {

  // Current status: 
  // 
  // 2017.12.14  Generating valid JSON code that can be read back in for tested files.
  //

  private Map<String, Object> moBases = new Hashtable<String, Object>();

  private boolean filterMOs;

  private Viewer vwr;

  public void set(Viewer viewer, OutputStream os) {
    vwr = viewer;
    setWriteNullAsString(false);
    setStream(os);
  }

  @Override
  public String toString() {
    return (oc == null ? "{}" : oc.toString());
  }

  public void writeJSON() {
    openSchema();
    writeMagic();
    oc.append(",\n");
    writeSchemaMetadata();
    writeJobs();
    closeSchema();
  }

  public void writeSchemaMetadata() {
    mapOpen();
    mapAddKeyValue("__jmol_created", new Date(), ",\n");
    mapAddKeyValue("__jmol_source", vwr.getP("_modelFile"), "");
    mapClose();
  }

  public void openSchema() {
    arrayOpen(false);
  }

  public void writeMagic() {
    writeString(QCSchemaUnits.version);
  }

  public void closeSchema() {
    oc.append("\n");
    arrayClose(false);
    closeStream();
  }

  public void writeJobs() {
    // only one job in Jmol
    writeJob(1);
  }

  public void writeJob(int iJob) {
    append(",\n");
    mapOpen();
    {
      mapAddKeyValue("__jmol_block", "Job " + iJob, ",\n");
      writeJobMetadata();
      writeModels();
      writeMOBases();
    }
    mapClose();
  }

  public void writeJobMetadata() {
    mapAddKey("metadata");
    mapOpen();
    {
      mapAddMapAllExcept("__jmol_info", vwr.getModelSetAuxiliaryInfo(),
          ";group3Counts;properties;group3Lists;models;unitCellParams;");
    }
    mapClose();
  }

  public void writeModels() {
    int nModels = vwr.ms.mc;
    oc.append(",\n");
    mapAddKey("steps");
    arrayOpen(true);
    {
      oc.append("\n");
      for (int i = 0; i < nModels;) {
        if (i > 0)
          append(",\n");
        i = writeModel(i);
      }
    }
    arrayClose(true);
  }

  public int writeModel(int modelIndex) {
    int nextModel = modelIndex + 1;
    append("");
    mapOpen();
    {
      mapAddKeyValue("__jmol_block", "Model " + (modelIndex + 1), ",\n");
      writeTopology(modelIndex);
      if (isVibration(modelIndex)) {
        oc.append(",\n");
        nextModel = writeVibrations(modelIndex);
      }
      if (haveMOData(modelIndex)) {
        oc.append(",\n");
        writeMOData(modelIndex);
      }
      oc.append(",\n");
      writeModelMetadata(modelIndex);
    }
    mapClose();
    oc.append("\n");
    return nextModel;
  }

  public void writeTopology(int modelIndex) {
    mapAddKey("topology");
    mapOpen();
    {
      writeAtoms(modelIndex);
      writeBonds(modelIndex);
    }
    mapClose();
  }

  public Object getProperty(int modelIndex, String key) {
    @SuppressWarnings("unchecked")
    Map<String, Object> props = (Map<String, Object>) (modelIndex >= vwr.ms.am.length ? null
        : vwr.ms.am[modelIndex].auxiliaryInfo.get("modelProperties"));
    return (props == null ? null : props.get(key));
  }

  private boolean isVibration(int modelIndex) {
    return (vwr.ms.getLastVibrationVector(modelIndex, 0) >= 0);
  }

  public void writeModelMetadata(int modelIndex) {
    mapAddKey("metadata");
    mapOpen();
    {
      mapAddMapAllExcept("__jmol_info", vwr.ms.am[modelIndex].auxiliaryInfo,
          ";.PATH;PATH;fileName;moData;unitCellParams;");
    }
    mapClose();
  }

  public void writeAtoms(int modelIndex) {
    SparseArray symbols = new SparseArray("_RLE_");
    SparseArray numbers = new SparseArray("_RLE_");
    SparseArray charges = new SparseArray("_RLE_");
    SparseArray names = new SparseArray("_RLE_");
    SparseArray types = new SparseArray("_RLE_");
    mapAddKey("atoms");
    mapOpen();
    {
      SymmetryInterface unitCell = vwr.ms.getUnitCell(modelIndex);
      boolean isFractional = (unitCell != null && !unitCell.isBio());
      if (isFractional) {
        float[] params = unitCell.getUnitCellAsArray(false);
        writePrefix_Units("unit_cell", "angstroms");
        mapAddKeyValue("unit_cell", params, ",\n");
      }
      writePrefix_Units("coords", isFractional ? "fractional" : "angstroms");
      mapAddKey("coords");
      arrayOpen(true);
      {
        oc.append("\n");
        BS bs = vwr.getModelUndeletedAtomsBitSet(modelIndex);
        int last = bs.length() - 1;
        P3 pt = new P3();
        for (int i = bs.nextSetBit(0); i >= 0; i = bs.nextSetBit(i + 1)) {
          Atom a = vwr.ms.at[i];
          append("");
          pt.setT(a);
          if (isFractional)
            unitCell.toFractional(pt, false);
          oc.append(formatNumber(pt.x)).append(",\t")
              .append(formatNumber(pt.y)).append(",\t")
              .append(formatNumber(pt.z)).append(i < last ? ",\n" : "\n");
          symbols.add(PT.esc(a.getElementSymbol()));
          numbers.add("" + a.getElementNumber());
          charges.add("" + a.getPartialCharge());
          String name = a.getAtomName();
          names.add(name);
          String type = a.getAtomType();
          types.add(type.equals(name) ? null : type);
        }
      }
      arrayClose(true);
      oc.append(",\n");
      if (charges.isNumericAndNonZero()) {
        mapAddKeyValueRaw("charge", charges, ",\n");
      }
      if (types.hasValues()) {
        mapAddKeyValueRaw("types", types, ",\n");
      }
      mapAddKeyValueRaw("symbol", symbols, ",\n");
      mapAddKeyValueRaw("atom_number", numbers, "\n");
    }
    mapClose();
  }

  private String formatNumber(float x) {
    return (x < 0 ? "" : " ") + DF.formatDecimal(x, -6);
  }

  private void writePrefix_Units(String prefix, String units) {
    mapAddKeyValueRaw(prefix + "_units", QCSchemaUnits.getUnitsJSON(units, false),
        ",\n");
  }

  public void writeBonds(int modelIndex) {
    // TODO
  }

  public int writeVibrations(int modelIndex) {
    mapAddKey("vibrations");
    arrayOpen(true);
    {
      oc.append("\n");
      String sep = null;
      int ivib = 0;
      modelIndex--;
      while (isVibration(++modelIndex)) {
        if (sep != null)
          oc.append(sep);
        sep = ",\n";
        append("");
        mapOpen();
        {
          mapAddKeyValue("__jmol_block", "Vibration " + (++ivib), ",\n");
          Object value = getProperty(modelIndex, "FreqValue");
          String freq = (String) getProperty(modelIndex, "Frequency");
          String intensity = (String) getProperty(modelIndex, "IRIntensity");
          String[] tokens;
          if (value == null) {
            System.out.println("model " + modelIndex
                + " has no _M.properties.FreqValue");
          }
          if (freq == null) {
            System.out.println("model " + modelIndex
                + " has no _M.properties.Frequency");
          } else {
            tokens = PT.split(freq, " ");
            if (tokens.length == 1) {
              System.out.println("model " + modelIndex
                  + " has no frequency units");
            }
            writeMapKeyValueUnits("frequency", value, tokens[1]);
          }
          if (intensity != null) {
            tokens = PT.split(intensity, " ");
            writeMapKeyValueUnits("ir_intensity", tokens[0], tokens[1]);

          }
          String label = (String) getProperty(modelIndex, "FrequencyLabel");
          if (label != null)
            mapAddKeyValue("label", label, ",\n");
          mapAddKey("vectors");
          arrayOpen(true);
          {
            oc.append("\n");
            BS bs = vwr.getModelUndeletedAtomsBitSet(modelIndex);
            int last = bs.length() - 1;
            for (int i = bs.nextSetBit(0); i >= 0; i = bs.nextSetBit(i + 1)) {
              Atom a = vwr.ms.at[i];
              Vibration v = a.getVibrationVector();
              append("");
              oc.append(formatNumber(v.x)).append(",\t")
                  .append(formatNumber(v.y)).append(",\t")
                  .append(formatNumber(v.z)).append(i < last ? ",\n" : "\n");
            }
          }
          arrayClose(true);
        }
        append("");
        mapClose();
      }
    }
    oc.append("\n");
    arrayClose(true);
    return modelIndex;
  }

  private void writeMapKeyValueUnits(String key, Object value, String units) {
    mapAddKeyValueRaw(key, "{\"value\":" + value + ",\"units\":"
        + QCSchemaUnits.getUnitsJSON(units, false) + "}", ",\n");
  }

  private boolean haveMOData(int modelIndex) {
    return (getAuxiliaryData(modelIndex, "moData") != null);
  }

  private Object getAuxiliaryData(int modelIndex, String key) {
    return vwr.ms.am[modelIndex].auxiliaryInfo.get(key);
  }

  private int basisID = 0;
  private Lst<int[]> shells;

  private int[][] dfCoefMaps;

  private void writeMOData(int modelIndex) {
    @SuppressWarnings("unchecked")
    Map<String, Object> moData = (Map<String, Object>) getAuxiliaryData(
        modelIndex, "moData");
    Map<String, Object> moDataJSON = new Hashtable<String, Object>();
    moDataJSON.put("orbitals", moData.get("mos"));
    // units
    String units = (String) moData.get("EnergyUnits");
    if (units == null)
      units = "?";
    moDataJSON.put("orbitals_energy_units", QCSchemaUnits.getUnitsJSON(units, true));
    // normalization is critical for Molden, NWChem, and many other readers.
    // not needed for Gaussian, Jaguar, WebMO, Spartan, or GenNBO
    moDataJSON.put("__jmol_normalized",
        Boolean.valueOf(moData.get("isNormalized") == Boolean.TRUE));
    String type = (String) moData.get("calculationType");
    moDataJSON.put("__jmol_calculation_type", type == null ? "?" : type);
    //    @SuppressWarnings("unchecked")
    //    Map<String, String> orbitalMaps = (Map<String, String>) moData.get("orbitalMaps");
    //    if (orbitalMaps != null && !orbitalMaps.isEmpty()) {
    //      moDataJSON.put("jmol_orbital_maps", orbitalMaps);      
    //    }
    moDataJSON.put("basis_id", getBasisID(moData));
    filterMOs = true;
    setModifyKeys(fixIntegration());
    mapAddKeyValue("molecular_orbitals", moDataJSON, "\n");
    setModifyKeys(null);
    filterMOs = false;
    append("");
  }

  private static Map<String, String> integrationKeyMap;

  /**
   * When an MO is calculated in Jmol, Jmol will check the integration so that
   * it can be checked to be close to 1.0000. This integration value is saved
   * back in the MO data, but it is not a standard key. (As though anything is
   * here!)
   * 
   * So we set a key mapping to replace it.
   * 
   * @return the "integration" key map
   */
  private static Map<String, String> fixIntegration() {
    if (integrationKeyMap == null) {
      integrationKeyMap = new Hashtable<String, String>();
      integrationKeyMap.put("integration", "__jmol_integration");
    }
    return integrationKeyMap;
  }

  @Override
  protected Object getAndCheckValue(Map<String, Object> map, String key) {
    if (filterMOs) {
      if (key.equals("dfCoefMaps"))
        return null;
      if (key.equals("symmetry"))
        return ((String) map.get(key)).replace('_', ' ').trim();
      if (key.equals("coefficients") && dfCoefMaps != null) {
        return fixCoefficients((double[]) map.get(key));
      }

    }
    return map.get(key);
  }

  /**
   * Jmol allows for a set of arrays that map coefficient indicies with
   * nonstandard order to Gaussian/Molden order. Here we do the conversion upon
   * writing so that the order is always Gaussian/Molden order.
   * 
   * @param coeffs
   * @return
   */
  private Object fixCoefficients(double[] coeffs) {
    double[] c = new double[coeffs.length];
    for (int i = 0, n = shells.size(); i < n; i++) {
      int[] shell = shells.get(i);
      int type = shell[1];
      int[] map = dfCoefMaps[type];
      for (int j = 0, coefPtr = 0; j < map.length; j++, coefPtr++)
        c[coefPtr + j] = coeffs[coefPtr + map[j]];
    }
    return c;
  }

  @SuppressWarnings("unchecked")
  private String getBasisID(Map<String, Object> moData) {
    String hash = "!";
    dfCoefMaps = (int[][]) moData.get("dfCoefMaps");
    if (dfCoefMaps != null) {
      // just looking for a non-zero map
      boolean haveMap = false;
      for (int i = 0; !haveMap && i < dfCoefMaps.length; i++) {
        int[] m = dfCoefMaps[i];
        for (int j = 0; j < m.length; j++)
          if (m[j] != 0) {
            haveMap = true;
            break;
          }
      }
      if (!haveMap)
        dfCoefMaps = null;
    }
    Object gaussians = moData.get("gaussians");
    if (gaussians != null) {
      hash += gaussians.hashCode();
    }
    shells = (Lst<int[]>) moData.get("shells");
    if (shells != null) {
      hash += shells.hashCode();
    }
    Object slaters = moData.get("slaters");
    if (slaters != null) {
      hash += slaters.hashCode();
    }
    String key = (String) moBases.get(hash);
    if (key == null) {
      moBases.put(hash, key = "MOBASIS_" + ++basisID);
      Map<String, Object> map = new Hashtable<String, Object>();
      if (gaussians != null) {
        map.put("gaussians", gaussians);
      }
      if (shells != null) {

        // shells array: [iAtom, type, gaussianPtr, gaussianCount]
        //
        // where type is one of:
        //
        //        final public static int S = 0;
        //        final public static int P = 1;
        //        final public static int SP = 2;
        //        final public static int DS = 3;
        //        final public static int DC = 4;
        //        final public static int FS = 5;
        //        final public static int FC = 6;
        //        final public static int GS = 7;
        //        final public static int GC = 8;
        //        final public static int HS = 9;
        //        final public static int HC = 10;
        //        final public static int IS = 11;
        //        final public static int IC = 12;

        // Note that this is currently implemented in Jmol with reference to a 
        // coefficient map that allows us to maintain the file-based MO ordering
        // and only map the actual coefficient to the function at MO creation time.

        map.put("shells", shells);
      }
      if (slaters != null) {
        map.put("slaters", slaters);
      }
      moBases.put(key, map);
    }
    return key;
  }

  public void writeMOBases() {
    if (moBases.isEmpty())
      return;
    oc.append(",\n");
    mapAddKey("mo_bases");
    mapOpen();
    {
      String sep = "";
      for (String key : moBases.keySet()) {
        if (key.startsWith("!"))
          continue;
        append(sep);
        mapAddKeyValue(key, moBases.get(key), "\n");
        sep = ",";
      }
    }
    mapClose();
    moBases.clear();
  }

  @Override
  public void writeObject(Object o) {
    if (o instanceof SlaterData) {
      oc.append(o.toString());
    } else {
      super.writeObject(o);
    }
  }

  //// sparse array handling ////
  public class SparseArray extends SB {
    private int repeatCount = 0;
    private int elementCount = 0;
    private String lastElement = null;
    private String sep = "";
    private String type; // _RLE_
    private boolean isRLE;

    public SparseArray(String type) {
      this.type = type;
      isRLE = (type.equals("_RLE_"));
    }

    protected void add(String element) {
      if (element == null)
        element = "null";
      if (!isRLE) {
        append(sep);
        append(element);
        sep = ",";
        return;
      }
      if (repeatCount > 0 && !element.equals(lastElement)) {
        append(sep);
        appendI(repeatCount);
        sep = ",";
        append(sep);
        append(lastElement);
        repeatCount = 0;
      }
      lastElement = element;
      repeatCount++;
      elementCount++;
    }

    public String lastElement() {
      return lastElement;
    }

    public boolean isEmpty() {
      return (elementCount == 0);
    }

    public boolean allNaN() {
      return (allSame() && PT.parseFloat(lastElement) == Float.NaN);
    }

    public boolean allNull() {
      return (allSame() && lastElement.equals("null"));
    }

    public boolean allEmptyString() {
      return (allSame() && lastElement.equals(""));
    }

    public boolean allSame() {
      return (!isEmpty() && elementCount == repeatCount);
    }

    public boolean allZero() {
      return (allSame() && PT.parseFloat(lastElement) != Float.NaN);
    }

    public boolean hasValues() {
      return (!allSame() || !allNull() && !allEmptyString());
    }

    public boolean isNumericAndNonZero() {
      return (allSame() && !allNaN() && !allZero());
    }

    @Override
    public String toString() {
      String s = super.toString();
      return (s.length() == 0 ? "[]" : "[\"" + type + "\"," + s
          + (repeatCount > 0 ? sep + repeatCount + "," + lastElement : "")
          + "]");
    }
  }

}
