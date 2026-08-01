package org.jmol.adapter.readers.quantum;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Hashtable;
import java.util.Map;

import javajs.util.AU;
import javajs.util.Lst;
import javajs.util.SB;

import org.jmol.adapter.smarter.Atom;
import org.jmol.api.JmolAdapter;
import org.jmol.util.Logger;
import org.qcschema.QCSchemaUnits;

/**
 * A molecular structure and orbital reader for MolDen files.
 * See http://www.cmbi.ru.nl/molden/molden_format.html
 * 
 * updated by Bob Hanson <hansonr@stolaf.edu> for Jmol 12.0/12.1
 * 
 * adding [spacegroup] [operators] [cell] [cellaxes] for Jmol 14.3.7 
 * 
 * @author Matthew Zwier <mczwier@gmail.com>
 */

public class QCJSONReader extends MoldenReader {
  
  private Map<String, Object> job;

  private int jobCount;

  private int modelCount;
  
  @SuppressWarnings("unchecked")
  @Override
  protected void initializeReader() {
    super.initializeReader();
    SB sb  = new SB();
    try {
      while (rd() != null)
        sb.append(line);
      Lst<Object> json = vwr.parseJSONArray(sb.toString());
      // first record is version tag
      Logger.info(json.get(0).toString());
      // second record is Jmol info; not used here
      jobCount = json.size() - 2;
      for (int i = 0; i < jobCount; i++)
        processJob((Map<String, Object>)json.get(i + 2));
    } catch (Exception e) {
      e.printStackTrace();
    }
    continuing = false;
  }

  /**
   * @param job 
   * @throws Exception 
   */
  private void processJob(Map<String, Object> job) throws Exception {
    this.job = job;
    readSteps();
    /*
    if (loadVibrations)
      readFreqsAndModes();
    if (loadGeometries)
      readGeometryOptimization();
    checkSymmetry();
    if (asc.atomSetCount == 1 && moData != null)
      finalizeMOData(moData);
      */
 }

  @Override
  public void finalizeSubclassReader() throws Exception {
    finalizeReaderASCR();
  }
  
  private void readSteps() throws Exception {
    ArrayList<Object> steps = QCSchemaUnits.getList(job, "steps");
    int nSteps = steps.size();
    for (int iStep = 0; iStep < nSteps; iStep++) {
      if (!doGetModel(++modelCount, null)) {
        if (!checkLastModel())
          return;
        continue;
      }
      asc.newAtomSet();
      @SuppressWarnings("unchecked")
      Map<String, Object> step = (Map<String, Object>) steps.get(iStep);
      Map<String, Object> topology = getMapSafely(step, "topology");
      Map<String, Object> atoms = getMapSafely(topology, "atoms");

      // one or the other of these is required:
      String[] symbols = QCSchemaUnits.getStringArray(atoms, "symbol");
      int[] atomNumbers = QCSchemaUnits.getIntArray(atoms, "atom_number");
      String[] atom_names = QCSchemaUnits.getStringArray(atoms, "atom_names");

      double[] coords = QCSchemaUnits.getDoubleArray(atoms, "coords");
      modelAtomCount = coords.length / 3;
      double f = QCSchemaUnits.getConversionFactor(atoms, "coords", QCSchemaUnits.UNITS_ANGSTROMS);
      boolean isFractional = (f == 0);
      setFractionalCoordinates(isFractional);
      if (isFractional) {
        f = QCSchemaUnits.getConversionFactor(atoms, "unit_cell", QCSchemaUnits.UNITS_ANGSTROMS);
        double[] cell = QCSchemaUnits.getDoubleArray(atoms, "unit_cell");
        // a b c alpha beta gamma 
        // m.m00, m.m10, m.m20, // Va
        // m.m01, m.m11, m.m21, // Vb
        // m.m02, m.m12, m.m22, // Vc
        // dimension, (float) volume,
        if (cell == null) {
          Logger.error("topology.unit_cell is missing even though atoms are listed as fractional");
        } else {
          for (int i = 0; i < 6; i++) {
            switch (i) {
            case 3:
              f = 1;
              //$FALL-THROUGH$
            default:
              setUnitCellItem(i, (float)(cell[i] * f));
              break;
            }
          }
        }
      }
      for (int i = 0, pt = 0; i < modelAtomCount; i++) {
        Atom atom = asc.addNewAtom();
        setAtomCoordXYZ(atom, (float)(coords[pt++] * f), (float)(coords[pt++] * f), (float) (coords[pt++]
            * f));
        String sym = (symbols == null ? JmolAdapter
            .getElementSymbol(atomNumbers[i]) : symbols[i]);
        atom.atomName = (atom_names == null ? sym : atom_names[i]);
        atom.elementNumber = (short) (atomNumbers == null ? JmolAdapter
            .getElementNumber(sym) : atomNumbers[i]);
      }
      if (doReadMolecularOrbitals) {
        readMolecularOrbitals(getMapSafely(step, "molecular_orbitals"));
        clearOrbitals();
      }
      applySymmetryAndSetTrajectory();
      if (loadVibrations) {
        readFreqsAndModes(QCSchemaUnits.getList(step, "vibrations"));
      }
      
    }
  }
  
  private boolean readFreqsAndModes(ArrayList<Object> vibrations) throws Exception {
    //  "frequency":{"value":-0.00,"units":["cm^-1","?"]},
    //      "ir_intensity":{"value":0.000005,"units":["au",1]},
    //    "vectors":[

    if (vibrations != null) {
      int n = vibrations.size();
      for (int i = 0; i < n; i++) {
        @SuppressWarnings("unchecked")
        Map<String, Object> vib = (Map<String, Object>) vibrations.get(i);
        double freq = QCSchemaUnits.getDouble(vib, "frequency", QCSchemaUnits.UNITS_CM_1);
        double[] vectors = QCSchemaUnits.getDoubleArray(vib, "vectors");
        if (i > 0)
          asc.cloneLastAtomSet();
        asc.setAtomSetFrequency(null, null, "" + freq, QCSchemaUnits.UNITS_CM_1);
        int i0 = asc.getLastAtomSetAtomIndex();
        for (int j = 0, pt = 0; j < modelAtomCount; j++) {
          asc.addVibrationVector(j + i0, (float) (vectors[pt++] * ANGSTROMS_PER_BOHR),
              (float) (vectors[pt++] * ANGSTROMS_PER_BOHR), (float) (vectors[pt++]
                  * ANGSTROMS_PER_BOHR));
        }
      }
    }
    return true;
  }
  
  private boolean haveEnergy = true;
  
  /**
   * Read basis and orbital information.
   * 
   * @param molecular_orbitals
   * @return true if successful
   * 
   * @throws Exception
   */
  private boolean readMolecularOrbitals(Map<String, Object> molecular_orbitals) throws Exception {
    if (molecular_orbitals == null)
      return false;
    String moBasisID = molecular_orbitals.get("basis_id").toString();//:"MOBASIS_1"
    if (!readBasis(moBasisID))
      return false;
    Boolean isNormalized = (Boolean) molecular_orbitals.get("__jmol_normalized");
    if (isNormalized != null && isNormalized.booleanValue())
      moData.put("isNormalized", isNormalized);
    calculationType = (String) molecular_orbitals.get("__jmol_calculation_type");
    if (calculationType == null)
      calculationType = "?";
    moData.put("calculationType", calculationType);

    ArrayList<Object> mos = QCSchemaUnits.getList(molecular_orbitals, "orbitals");
    int n = mos.size();
    for (int i = 0; i < n; i++) {
      @SuppressWarnings("unchecked")
      Map<String, Object> thisMO = (Map<String, Object>) mos.get(i); 
      double energy = QCSchemaUnits.getDouble(thisMO, "energy", "ev");
      double occupancy = QCSchemaUnits.getDouble(thisMO, "occupancy", null);
      String symmetry = (String) thisMO.get("symmetry");
      String spin = (String) thisMO.get("type");
      if (spin != null) {
        if (spin.indexOf("beta") >= 0)
          alphaBeta = "beta";
        else if (spin.indexOf("alpha") >= 0)
          alphaBeta = "alpha";
      }
      float[] coefs = toFloatArray(QCSchemaUnits.getDoubleArray(thisMO, "coefficients"));
      line = "" + symmetry;
      if (filterMO()) {
        Map<String, Object> mo = new Hashtable<String, Object>();
        mo.put("coefficients", coefs);
        if (Double.isNaN(energy)) {
          haveEnergy = false;
        } else {
          mo.put("energy", Float.valueOf((float) energy));
        }
        if (!Double.isNaN(occupancy))
          mo.put("occupancy", Float.valueOf((float) occupancy));
        if (symmetry != null)
          mo.put("symmetry", symmetry);
        if (alphaBeta.length() > 0)
          mo.put("type", alphaBeta);
        setMO(mo);
        if (debugging) {
          Logger.debug(coefs.length + " coefficients in MO " + orbitals.size());
        }
      }
    }
    if (debugging)
      Logger.debug("read " + orbitals.size() + " MOs");
    ArrayList<Object> units = QCSchemaUnits.getList(molecular_orbitals, "orbitals_energy_units");
    String sunits = (units == null ? null : units.get(0).toString());
    setMOs(sunits == null || sunits.equals("?") ? "?" : sunits);
    if (haveEnergy && doSort)
      sortMOs();
    return false;
  }
  
  private float[] toFloatArray(double[] da) {
    float[] fa = new float[da.length]; 
    for (int j = da.length; --j >= 0;)
      fa[j] = (float) da[j];
    return fa;
  }

  String lastBasisID = null;
  private boolean readBasis(String moBasisID) throws Exception {
    Map<String, Object> moBasisData = getMapSafely(job, "mo_bases");
    Map<String, Object> moBasis = getMapSafely(moBasisData, moBasisID);
    if (moBasis == null) {
      Logger.error("No job.mo_bases entry for " + moBasisID);
      return false;
    }
    if (moBasisID == lastBasisID)
      return true;
    lastBasisID = moBasisID;
    ArrayList<Object> listG = QCSchemaUnits.getList(moBasis, "gaussians");
    ArrayList<Object> listS = QCSchemaUnits.getList(moBasis, "shells");
    if (listG == null && listS == null) {
      listG = listS = QCSchemaUnits.getList(moBasis, "slaters");
    }
    if ((listG == null) != (listS == null)) {
      Logger.error("gaussians/shells or slaters missing");
      return false;
    }
    if (listG == listS) {
      readSlaterBasis(listS);
    } else {
      readGaussianBasis(listG, listS);
    }
    return true;
  }

  boolean readSlaterBasis(ArrayList<Object> listS) throws Exception {
    /*
    1    0    0    0    1             1.5521451600        0.9776767193          
    1    1    0    0    0             1.5521451600        1.6933857512          
    1    0    1    0    0             1.5521451600        1.6933857512          
    1    0    0    1    0             1.5521451600        1.6933857512          
    2    0    0    0    0             1.4738648100        1.0095121222          
    3    0    0    0    0             1.4738648100        1.0095121222          
     */
    
    nCoef = listS.size();
    for (int i = 0; i < nCoef; i++) {
      double[] a = QCSchemaUnits.getDoubleArray(listS.get(i), null);
      addSlater((int) a[0], (int) a[1], (int) a[2], (int) a[3], (int) a[4], (float) a[5], (float) a[6]);
    }
    setSlaters(false, false);
    return true;
  }

  private boolean readGaussianBasis(ArrayList<Object> listG, ArrayList<Object> listS) throws Exception {
    shells = new Lst<int[]>();
    for (int i = 0; i < listS.size(); i++)
      shells.addLast(QCSchemaUnits.getIntArray(listS.get(i), null));
    int gaussianPtr = listG.size();
    float[][] garray = AU.newFloat2(gaussianPtr);
    // [[exp, coef], [exp, coef],...] with sp [exp, coef1, coef2]
    for (int i = 0; i < gaussianPtr; i++)
      garray[i] = toFloatArray(QCSchemaUnits.getDoubleArray(listG.get(i), null)); 
    moData.put("shells", shells);
    moData.put("gaussians", garray);
    Logger.info(shells.size() + " slater shells read");
    Logger.info(garray.length + " gaussian primitives read");
    //Logger.info(nCoef + " MO coefficients expected for orbital type " + orbitalType);
    asc.setCurrentModelInfo("moData", moData);
    return false;
  }
 
  @SuppressWarnings("unchecked")
  private void sortMOs() {
    Object[] list = orbitals.toArray(new Object[orbitals.size()]);
    Arrays.sort(list, new MOEnergySorter());
    orbitals.clear();
    for (int i = 0; i < list.length; i++)
      orbitals.addLast((Map<String, Object>)list[i]);
  }

  /**
   * Safely get a Map from a Map using a key.
   * @param map
   * @param key
   * @return the Map or null
   */
  @SuppressWarnings("unchecked")
  private static Map<String, Object> getMapSafely(Map<String, Object> map, String key) {
    return (map == null ? null : (Map<String, Object>) map.get(key));
  }

  /////////////////// from Molden reader -- TODO /////////////////
  
//  private boolean checkSymmetry() throws Exception {
//    // extension for symmetry
//    if (line.startsWith("[SPACEGROUP]")) {
//      setSpaceGroupName(rd());
//      rd();
//      return true;
//    }
//    if (line.startsWith("[OPERATORS]")) {
//      while (rd() != null && line.indexOf("[") < 0)
//        if (line.length() > 0) {
//          Logger.info("adding operator " + line);
//          setSymmetryOperator(line);
//        }
//      return true;
//    }
//    if (line.startsWith("[CELL]")) {
//      rd();
//      Logger.info("setting cell dimensions " + line);
//      // ANGS assumed here
//      next[0] = 0;
//      for (int i = 0; i < 6; i++)
//        setUnitCellItem(i, parseFloat());
//      rd();
//      return true;
//    }
//    if (line.startsWith("[CELLAXES]")) {
//      float[] f = new float[9];
//      fillFloatArray(null, 0, f);
//      addExplicitLatticeVector(0, f, 0);
//      addExplicitLatticeVector(1, f, 3);
//      addExplicitLatticeVector(2, f, 6);
//      return true;
//    }
//    return false;
//  }
//
}
