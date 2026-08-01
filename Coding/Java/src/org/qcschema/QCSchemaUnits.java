package org.qcschema;

import java.util.Hashtable;
import java.util.Map;

import java.util.ArrayList;

import org.jmol.viewer.Viewer;

/**
 * A general Java class for working with QCShema units and array types.
 * 
 * j2sNative blocks can be ignored -- they just increase efficiency in the JavaScript rendition of Jmol.
 *  
 */
public class QCSchemaUnits {

  public final static String version = "QCJSON 0-0-0.Jmol_"
      + Viewer.getJmolVersion().replace(' ', '_');

  // 
  //  source: http://cccbdb.nist.gov/hartree.asp
  //  A hartree is equal to 2625.5 kJ/mol, 627.5 kcal/mol, 27.211 eV, and 219474.6 cm-1.
  //  One bohr = 0.529 177 210 67 x 10-10 m 
  
  public final static String UNITS_FRACTIONAL = "fractional";

  public final static String UNITS_AU = "au";
  public final static double TOAU_AU = 1;
  
  // distance
  
  public final static String UNITS_CM = "cm";
  public final static double TOAU_CM = 1/0.52917721067e-8;
  
  public final static String UNITS_M = "m";
  public final static double TOAU_M = 1/0.52917721067e-10;
  
  public final static String UNITS_ANGSTROMS = "angstroms";
  public final static double TOAU_ANGSTROMS = 1/0.52917721067; // 1.88972613;
  
  public final static String UNITS_BOHR = "bohr";
  public final static double TOAU_BOHR = 1;
  
  // energy
  
  public final static String UNITS_HARTREE = "hartree";
  public final static double TOAU_HARTREE = 1;
  
  public final static String UNITS_EV = "ev";
  public final static double TOAU_EV = 1/27.211; //0.03688675765;
  
  public final static String UNITS_CM_1 = "cm-1";
  public final static double TOAU_CM_1 = 1/219474.6; //4.5563359e-6;
  
  public final static String UNITS_KJ_MOL = "kj/mol";
  public final static double TOAU_KJ_MOL = 1/2635.5;  //0.00038087983;  
  
  public final static String UNITS_KCAL_MOL = "kcal/mol";
  public final static double TOAU_KCAL_MOL = 1/627.5; //0.00159362549;
  
  /**
   * A very simple and efficient way to catalog string matches. Far faster than ENUM.
   * Note that singular or plural on anstroms, bohrs, or hartrees both work.
   */
  private final static String knownUnits =
  /////0         1         2         3         4         5         6         7         8
  /////012345678901234567890123456789012345678901234567890123456789012345678901234567890123
      "cm cm^-1 cm-1 angstroms au atomic units fractional bohrs hartrees ev kj_mol kcal_mol";

  private static Hashtable<String, Double> htConvert = new Hashtable<String, Double>();
  
  /**
   * Get the standard conversion factor to atomic units for this unit.
   * 
   * @param units
   * @return the nominal conversion factor or 0 ("fractional") or Double.NaN (unknown)
   */
  public static double getFactorToAU(String units) {
    switch (knownUnits.indexOf(units.toLowerCase())) {
    case 0:
      // units = UNITS_CM
      return TOAU_CM;
    case 1:
      // units = UNITS_M
      return TOAU_M;
    case 3:
    case 9:
      //units = UNITS_CM_1;
      return TOAU_CM_1;
    case 14:
      //units = UNITS_ANGSTROMS;
      return TOAU_ANGSTROMS;
    case 24:
    case 27:
      //units = UNITS_AU;
      return 1;
    case 40:
      //units = "UNITS_FRACTIONAL";
      return 0;
    case 51:
      //units = UNITS_BOHR;
      return TOAU_BOHR;
    case 57:
      //units = UNITS_HARTREE;
      return TOAU_HARTREE;
    case 66:
      //units = UNITS_EV;
      return TOAU_EV;
    case 69:
      //units = UNITS_KCAL_MOL;
      return TOAU_KCAL_MOL;
    case 76:
      //units = UNITS_KJ_MOL;
      return TOAU_KJ_MOL;
    default:
      return Double.NaN;
    }
  }
  
  /**
   * Calculate the unit conversion between two units, using a static 
   * unit-to-unit cache for efficiency.
   * 
   * Not used in Jmol.
   * 
   * @param fromUnits
   * @param toUnits
   * @return conversion factor or Double.NaN if anything goes wrong.
   */
  public static double getUnitConversion(String fromUnits, String toUnits) {
    if (fromUnits.equalsIgnoreCase(toUnits))
      return 1;
    String key = "" + fromUnits + toUnits;
    Double d = htConvert.get(key);
    if (d != null)
      return d.doubleValue();
    double val = Double.NaN;
    try {
      double toAUDesired = getFactorToAU(toUnits);
      double toAUActual = getFactorToAU(fromUnits);
      val = toAUActual / toAUDesired;
    } catch (Exception e) {
      // just leave it as 1
    }
    htConvert.put(key,  Double.valueOf(val));
    return val;
  }

  /**
   * For a reader, use the JSON [units, factor] along with a desired unit to get the conversion
   * factor from file values to desired units.
   * 
   * Currently, this method only looks at the factor in the JSON if we do not already know the conversion factor. 
   * 
   * @param unitsFactor [units, factor] list or null if to AU is desired.
   * @param unitsDesired
   * @return the conversion factor or Double.NaN if not uncodable
   */
  public static double getConversionFactorTo(ArrayList<Object> unitsFactor, String unitsDesired) {
    try {
    double toAUDesired = getFactorToAU(unitsDesired);
    double toAUActual = getFactorToAU(unitsFactor == null ? UNITS_AU : unitsFactor.get(0).toString());
    if (Double.isNaN(toAUActual))
      toAUActual = Double.parseDouble(unitsFactor.get(1).toString());
    return toAUActual / toAUDesired;
    } catch (Exception e) {
      return Double.NaN;
    }
  }

  /**
   * Read a {value:xxxx, units:["name",toAU]} map, converting it to the desired units.
   * 
   * @param valueUnits
   * @param toUnits
   * @return converted value
   */
  public static double convertValue(Map<String, Object> valueUnits, String toUnits) {
      return getDouble(valueUnits, "value", null) * getConversionFactor(valueUnits, "units", toUnits);
  }

  /**
   * Get the [name, toAU] JSON code or just a new String[] {name, toAU}.
   * If the conversion is not known, return [name, "?"]
   * @param name
   * @param asArray
   * @return String or String[]
   */
  public static Object getUnitsJSON(String name, boolean asArray) {
    double d = getFactorToAU(name);
    String toAU = (!Double.isNaN(d) ? "" + d : asArray ? "?" :  "\"?\"");
    return (asArray ? new String[] { name, toAU } : "[\"" + name + "\","
        + toAU + "]");
  }


  /**
   * Get the necessary conversion factor to the desired units from a key_units or atomic units 
   * @param map
   * @param key map key that has associated key_units element or null for "from atomic units"
   * @param toUnits
   * @return conversion factor
   */
  public static double getConversionFactor(Map<String, Object> map, String key, String toUnits) {
    ArrayList<Object> list = getList(map, key + "_units");
    String units = (list == null ? null : list.get(0).toString());
    double f = getConversionFactorTo(list, toUnits);
    if (Double.isNaN(f)) {
      System.out.println("units for " + units + "? " + units);
      f = 1;
    }
    return f;
  }

  /**
   * Reads a value from an associative array, converting it to the desired units.
   * 
   * @param map
   * @param key
   * @param toUnits
   * @return value
   */
  @SuppressWarnings("unchecked")
  public static double getDouble(Map<String, Object> map, String key, String toUnits) {
    Object o = map.get(key);
    double conv = 1;
    if (toUnits != null)
      if (o instanceof Map<?, ?>) {
        //  "frequency":{"value":-0.00,"units":["cm^-1",4.5563359e-6]},
        return convertValue((Map<String, Object>) o, toUnits);
      } else if (map.containsKey(key + "_units")) {
        //  "frequency_units":["cm^-1",4.5563359e-6],
        //  "frequency":-0.00,
        conv = getConversionFactor(map, key, toUnits);
      }
    return (o == null ? Double.NaN : ((Number) o).doubleValue() * conv);
  }

  /**
   * Retrieve an array of any sort as a list of objects, possibly unpacking it
   * if it is run-length encoded.
   * 
   * @param mapOrList
   * @param key
   * @return unpacked array
   */
  public static ArrayList<Object> getList(Object mapOrList, String key) {
    @SuppressWarnings("unchecked")
    ArrayList<Object> list = (ArrayList<Object>) (key == null ? mapOrList
        : ((Map<String, Object>) mapOrList).get(key));
    if (list == null)
      return null;
    int n = list.size();
    if (n == 0 || !"_RLE_".equals(list.get(0)))
      return list;
    ArrayList<Object> list1 = newList();
    for (int i = 1; i < n; i++) {
      int count = ((Number) list.get(i)).intValue();
      Object value = list.get(++i);
      for (int j = 0; j < count; j++)
      /**
       * j2s avoids overloaded add() for speed
       * 
       * @j2sNative list1.addLast(value);
       */
      {
        list1.add(value);
      }
    }
    return list1;
  }

  /**
   * @return ArrayList, or in JavaScript javajs.util.Lst
   *  
   * @j2sNative
   * 
   *  return new javajs.util.Lst();
   */
  protected static ArrayList<Object> newList() {
      return new ArrayList<Object>();
  }

  /**
   * Retrieve a double array, possibly unpacking it if it is run-length encoded.
   * Read any error as Double.NaN. 
   * 
   * @param mapOrList
   * @param key  into mapOrList, or null if mapOrList is a list
   * @return unpacked double[]
   */
  public static double[] getDoubleArray(Object mapOrList, String key) {
    ArrayList<Object> list = getList(mapOrList, key);
    if (list == null)
      return null;
    double[] a = new double[list.size()];
    for (int i = a.length; --i >= 0;) {
      try {
        a[i] = ((Number) list.get(i)).doubleValue();
      } catch (Exception e) {
        a[i] = Double.NaN;
      }
    }
    return a;
  }

  /**
   * Retrieve an int array, possibly unpacking it if it is run-length encoded.
   * Any error causes this method to return null.
   * 
   * @param mapOrList the list to unpack, or map to pull the list form using the key
   * @param key the map key, or null if mapOrList is already a list
   * @return unpacked int[] or null if mapOrList is null or there is an error
   */
  public static int[] getIntArray(Object mapOrList, String key) {
    ArrayList<Object> list = getList(mapOrList, key);
    if (list != null) {
      try {
    int[] a = new int[list.size()];
    for (int i = a.length; --i >= 0;)
      a[i] = ((Number) list.get(i)).intValue();
    return a;
      } catch (Exception e) {
        // return null in this case
      }
    }
    return null;
  }

  /**
   * Retrieve a String array, possibly unpacking it if it is run-length encoded.
   * Any "null" string is read as null. 
   * 
   * @param mapOrList the list to unpack, or map to pull the list form using the key
   * @param key the map key, or null if mapOrList is already a list
   * @return unpacked string[] or null if mapOrList is null
   */
  public static String[] getStringArray(Object mapOrList, String key) {
    ArrayList<Object> list = getList(mapOrList, key);
    if (list == null)
      return null;
    String[] a = new String[list.size()];
    for (int i = a.length; --i >= 0;) {
      Object o = list.get(i);
      a[i] = (o == null ? null : list.get(i).toString());
    }
    return a;
  }

//  static {
//    System.out.println(getUnitConversion("Angstroms", "cm"));
//    System.out.println(getUnitConversion("Angstroms", "bohr"));
//    System.out.println(getUnitConversion("bohr", "Angstroms"));
//    System.out.println(getUnitConversion("AX", "bohr"));
//    System.out.println(getUnitConversion("bohr", "AX"));
//  }
}
