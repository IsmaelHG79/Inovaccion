/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package com.axity.processors;

import com.google.common.hash.Hashing;
import org.apache.nifi.components.PropertyDescriptor;
import org.apache.nifi.flowfile.FlowFile;
import org.apache.nifi.annotation.documentation.CapabilityDescription;
import org.apache.nifi.expression.ExpressionLanguageScope;
import org.apache.nifi.annotation.documentation.Tags;
import org.apache.nifi.processor.exception.ProcessException;
import org.apache.nifi.processor.AbstractProcessor;
import org.apache.nifi.processor.ProcessContext;
import org.apache.nifi.processor.ProcessSession;
import org.apache.nifi.processor.ProcessorInitializationContext;
import org.apache.nifi.processor.Relationship;
import org.apache.nifi.processor.io.InputStreamCallback;
import org.apache.nifi.processor.io.OutputStreamCallback;
import org.apache.nifi.processor.util.StandardValidators;
import org.apache.poi.ss.usermodel.*;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;
import java.text.Normalizer;
import java.util.*;
import java.util.concurrent.atomic.AtomicReference;

@Tags({"XLSX","Read Excel File","Read","Excel","Flat XLSX","CSV"})
@CapabilityDescription("Custom Processor that handle XLSX Files")

public class FlatXLSXToCSV extends AbstractProcessor {

    ///init variables
    private static List<String> sheetNames = new ArrayList<>();
    private static Map<String, Map<Integer, String>> mapSheetData = new HashMap<>();
    private static  HashSet listSetsAllColumns=new HashSet();
    private static final String DESIRED_SHEETS_DELIMITER = ",";
    private static final String INIT_STR = "";
    private static final int INIT_COUNT =1;
    private static final String SHEET_NAME ="Sheet_Name";

    public static final PropertyDescriptor DESIRED_SHEETS = new PropertyDescriptor
            .Builder().name("extract-sheets")
            .displayName("Sheets to Extract")
            .description("Comma separated list of Excel document sheet names that should be extracted from the excel document. If this property" +
                    " is left blank then all of the sheets will be extracted from the Excel document. The list of names is case in-sensitive. Any sheets not " +
                    "specified in this value will be ignored.")
            .required(false)
            .expressionLanguageSupported(ExpressionLanguageScope.FLOWFILE_ATTRIBUTES)
            .addValidator(StandardValidators.NON_EMPTY_VALIDATOR)
            .build();

    public static final PropertyDescriptor CSV_SEPARATOR = new PropertyDescriptor
            .Builder().name("csv-split-separator")
            .displayName("Tag Split Separator of CSV Files")
            .description("Character to separate csv file")
            .required(true)
            .expressionLanguageSupported(ExpressionLanguageScope.FLOWFILE_ATTRIBUTES)
            .addValidator(StandardValidators.NON_EMPTY_VALIDATOR)
            .build();


    public static final PropertyDescriptor ROWS_TO_SKIP = new PropertyDescriptor
            .Builder().name("excel-extract-first-row")
            .displayName("Header Position Start")
            .description("The row number of the xlsx header position")
            .required(true)
            .defaultValue("0")
            .expressionLanguageSupported(ExpressionLanguageScope.FLOWFILE_ATTRIBUTES)
            .addValidator(StandardValidators.NON_NEGATIVE_INTEGER_VALIDATOR)
            .build();


    private static final Relationship SUCCESS = new Relationship.Builder()
            .name("success")
            .description("XLSX flattened to csv")
            .build();

    private static final Relationship FAILURE = new Relationship.Builder()
            .name("failure")
            .description("XLSX content that could not be processed")
            .build();


    private List<PropertyDescriptor> descriptors;

    private Set<Relationship> relationships;

    @Override
    protected void init(final ProcessorInitializationContext context) {
        final List<PropertyDescriptor> descriptors = new ArrayList<PropertyDescriptor>();
        descriptors.add(ROWS_TO_SKIP);
        descriptors.add(DESIRED_SHEETS);
        descriptors.add(CSV_SEPARATOR);
        this.descriptors = Collections.unmodifiableList(descriptors);

        final Set<Relationship> relationships = new HashSet<Relationship>();
        relationships.add(SUCCESS);
        relationships.add(FAILURE);

        this.relationships = Collections.unmodifiableSet(relationships);
    }

    @Override
    public Set<Relationship> getRelationships() {
        return this.relationships;
    }

    @Override
    public final List<PropertyDescriptor> getSupportedPropertyDescriptors() {
        return descriptors;
    }

    @Override
    public void onTrigger(final ProcessContext context, final ProcessSession session) throws ProcessException {

        final AtomicReference<String> value = new AtomicReference<>();

        FlowFile flowFile = session.get();
        if ( flowFile == null ) {
            return;
        }
        // get values
        final String desiredSheetsDelimited = context.getProperty(DESIRED_SHEETS).evaluateAttributeExpressions(flowFile).getValue();
        final int firstRow = context.getProperty(ROWS_TO_SKIP).evaluateAttributeExpressions(flowFile).asInteger();
        final String csvSeparetor = context.getProperty(CSV_SEPARATOR).evaluateAttributeExpressions(flowFile).getValue();

        try {
            session.read(flowFile, new InputStreamCallback() {
                @Override
                public void process(InputStream inputStream) throws IOException {
                    String xlsxToCsv = startConverssion(inputStream,desiredSheetsDelimited,firstRow,csvSeparetor);
                    value.set(xlsxToCsv);
                }
            });
        }catch (Exception e){
            getLogger().error("Failed to process incoming Excel document. " + e.getMessage(), e);
            FlowFile failedFlowFile = session.putAttribute(flowFile,
                    FlatXLSXToCSV.class.getName() + ".error", e.getMessage());
            session.transfer(failedFlowFile, FAILURE);
        }

        String results = value.get();
        if(results != null && !results.isEmpty()){

            flowFile = session.putAttribute( flowFile, "mime.type", "text/csv" );
            flowFile = session.putAttribute(flowFile, "csv", results);
        }

        flowFile = session.write(flowFile, new OutputStreamCallback() {

            @Override
            public void process(OutputStream out) throws IOException {
                out.write(value.get().getBytes());
            }
        });

        session.transfer(flowFile, SUCCESS);
    }

    private static  String cleanHeader(String header){
        String normalizer = Normalizer.normalize(header, Normalizer.Form.NFD).replaceAll("[^\\p{ASCII}]", "");
        String withoutSpace = normalizer.trim().replace(" ","_");
        String cleaned = withoutSpace.replaceAll("[{}()/]+","").replace("#","Num");
        return cleaned;
    }

    private  String startConverssion(InputStream inputStream ,String desiredSheetsDelimited,int rowStartIndex,String csvSeparetor) {

        String res =INIT_STR;
        Workbook workbook = null;
        try {

            workbook = WorkbookFactory.create(inputStream);
            workbook.setMissingCellPolicy(Row.MissingCellPolicy.RETURN_BLANK_AS_NULL);


            if (desiredSheetsDelimited != null) {
                String[] desiredSheets = desiredSheetsDelimited.split(DESIRED_SHEETS_DELIMITER);

                if (desiredSheets != null) {

                    for (int j=0; j<workbook.getNumberOfSheets(); j++) {
                        String sheetName = workbook.getSheetName(j);

                        for (int i = 0; i < desiredSheets.length; i++) {

                            if (sheetName.equalsIgnoreCase(desiredSheets[i])) {

                                sheetNames.add(sheetName);
                                Map<Integer, String> dataHeaders = getHeaders(workbook,sheetName,rowStartIndex);
                                mapSheetData.put(sheetName,dataHeaders);
                                break;
                            }
                        }
                    }

                    List<Map<String, String>> dataWithColsSerialized = handleExcel(mapSheetData,sheetNames,workbook,rowStartIndex);

                    res = mapToCSV(dataWithColsSerialized,csvSeparetor);

                } else {
                    getLogger().debug("Excel document was parsed but no sheets with the specified desired names were found.");
                }
            } else {

                for (int i=0; i<workbook.getNumberOfSheets(); i++) {

                    String sheetName = workbook.getSheetName(i);
                    sheetNames.add(sheetName);
                    Map<Integer, String> dataHeaders = getHeaders(workbook,sheetName,rowStartIndex);
                    mapSheetData.put(sheetName,dataHeaders);
                }

                List<Map<String, String>> dataWithColsSerialized = handleExcel(mapSheetData,sheetNames,workbook,rowStartIndex);

                res = mapToCSV(dataWithColsSerialized,csvSeparetor);
            }
        } catch (Exception e) {
            getLogger().error("error on workbook: "+ e.getMessage(), e);
        }
        finally {
            try {
                if(workbook != null)
                    workbook.close();
                if(inputStream != null)
                    inputStream.close();
                sheetNames.clear();
                mapSheetData.clear();
                listSetsAllColumns.clear();
            } catch (IOException e) {
                e.printStackTrace();
                getLogger().error("error: "+e.getMessage());
            }
        }
        return res;
    }

    private  Map<Integer, String> getHeaders(Workbook workbook, String sheetName, int rowStartIndex){
        Map<Integer, String> mapSheetCols = new HashMap<>();
        Workbook workbookTemp = workbook;

        try {
            Sheet sheet = workbookTemp.getSheet(sheetName);
            Iterator<Row> rowIterator = sheet.iterator();

            int count =INIT_COUNT;
            int celIndex = INIT_COUNT;
            while (rowIterator.hasNext()) {
                Row row = rowIterator.next();

                if (count == rowStartIndex){

                    Iterator<Cell> cellIterator = row.cellIterator();

                    while (cellIterator.hasNext()) {

                        Cell cell = cellIterator.next();

                        DataFormatter formatter = new DataFormatter();
                        String colName = formatter.formatCellValue(cell);

                        mapSheetCols.put(celIndex,colName);
                        celIndex++;
                    }
                    break;
                }
                count ++;
            }
        } catch (Exception e) {
            getLogger().error("error: "+ e.getMessage(), e);
        }
        finally {
            try {
                if(workbookTemp != null)
                    workbookTemp.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        return mapSheetCols;
    }

    public static<K,V> Map<K,V> clone(Map<K,V> original) {
        Map<K,V> copy = new HashMap<>();
        copy.putAll(original);
        return copy;
    }


    private static String mapToCSV(List<Map<String, String>> excelToMap , String csvSeparetor){

        HashSet<String> csvAllCols =  (HashSet)listSetsAllColumns.clone();

        StringBuilder csvToString = new StringBuilder();

        int indexHeader = INIT_COUNT;
        String headerTemp= INIT_STR;

        for (String col:csvAllCols) {
            headerTemp = headerTemp.concat(cleanHeader(col));
            if(indexHeader < csvAllCols.size())
                headerTemp= headerTemp.concat(csvSeparetor);
            indexHeader++;
        }
        csvToString.append(headerTemp);

        for (Map<String, String> dataRow: excelToMap) {
            int indexRowTemp = INIT_COUNT;
            String rowValTemp=INIT_STR;

            for (String col:csvAllCols) {

                String  colVal =dataRow.get(col);
                if(colVal == null){
                    colVal =INIT_STR;
                }
                rowValTemp = rowValTemp.concat(colVal);

                if(indexRowTemp < csvAllCols.size())
                    rowValTemp= rowValTemp.concat(csvSeparetor);

                indexRowTemp++;
            }
            csvToString.append("\n").append(rowValTemp);
        }
        return csvToString.toString();
    }

    private static String generateHash256(String commaSeparatedListOfColumns, Map<String, String> rowDataCompleteSerialized){

        String resHash = "";
        if(commaSeparatedListOfColumns != null && !commaSeparatedListOfColumns.equals("")){

            Collection<String> listKeyValues = rowDataCompleteSerialized.keySet();

            String[] listOfcommaSeparatedListOfColumns = commaSeparatedListOfColumns.split(",");

            listKeyValues.retainAll (Arrays.asList(listOfcommaSeparatedListOfColumns));

            Collection<String> listKeyValuesCopy = listKeyValues;
            int sizeListCopy = listKeyValuesCopy.size();

            if( sizeListCopy >= 2){
                Optional<String> colsValuesConcat = listKeyValues.stream().map(x -> rowDataCompleteSerialized.get(x)).reduce( (x, y) -> x.concat(y));
                resHash= colsValuesConcat.get();
            }else  if(sizeListCopy == 1){
                resHash =listKeyValues.toArray()[0].toString();
            }

            String sha256hex = Hashing.sha256()
                    .hashString(resHash, StandardCharsets.UTF_8)
                    .toString();

            resHash = sha256hex;
        }

        return resHash;
    }

    private  List<Map<String, String>>  handleExcel( Map<String, Map<Integer,String>> mapXlsxData , List<String> sheetNames,Workbook workbook, int indexStart ) throws IOException {

        Workbook workbookTemp = workbook;
        List<Map<String, String>> rowAllXLSXList = new ArrayList<>();

        try {
            for (String sheet: sheetNames   ) {
                Map<Integer,String> mapValues = mapXlsxData.get(sheet);
                Collection<String> mapKeys =mapValues.values();
                listSetsAllColumns.addAll(mapKeys); // es global en algun momento se tiene que vaciar
            }
            listSetsAllColumns.add(SHEET_NAME);

            for (String sheetName: sheetNames   ) {

                Map<Integer,String> sheetData = mapXlsxData.get(sheetName);
                Collection<String> headerList = sheetData.values();

                Sheet sheet = workbook.getSheet(sheetName);

                int countRow =1;
                for (int rn=sheet.getFirstRowNum(); rn<=sheet.getLastRowNum(); rn++) {

                    HashSet<String> listDiffTemp =  (HashSet)listSetsAllColumns.clone();
                    listDiffTemp.removeAll(headerList);

                    Row row = sheet.getRow(rn);
                    if (countRow > indexStart){

                        Map<String, String> rowDataCompleteSerialized = new HashMap<>();
                        if (row != null && row.getLastCellNum() > 0) {

                            for (int cn=0; cn<row.getLastCellNum(); cn++) {

                                Cell cell = row.getCell(cn);

                                if(cn+1 <= sheetData.size()){
                                    if (cell == null) {
                                        String value = "";
                                        String colName = sheetData.get(cn+1);
                                        rowDataCompleteSerialized.put(colName,value);
                                    } else {
                                        DataFormatter formatter = new DataFormatter();
                                        String value = formatter.formatCellValue(cell);
                                        String colName = sheetData.get(cn+1);
                                        rowDataCompleteSerialized.put(colName,value);
                                    }
                                }
                            }
                            for (String colDiff: listDiffTemp) {
                                rowDataCompleteSerialized.put(colDiff,"");
                            }
                            rowDataCompleteSerialized.put(SHEET_NAME,sheetName);
                            rowAllXLSXList.add(rowDataCompleteSerialized);
                        }
                    }
                    countRow++;
                }
            }
        } catch (Exception e) {
            getLogger().error("error: "+ e.getMessage(), e);
        }
        finally {
            if(workbookTemp != null)
                workbookTemp.close();
        }
        return rowAllXLSXList;
    }
}
