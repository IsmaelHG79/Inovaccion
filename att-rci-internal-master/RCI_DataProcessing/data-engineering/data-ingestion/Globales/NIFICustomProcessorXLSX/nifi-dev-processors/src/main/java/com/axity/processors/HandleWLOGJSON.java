package com.axity.processors;

import org.apache.nifi.annotation.documentation.CapabilityDescription;
import org.apache.nifi.annotation.documentation.Tags;
import org.apache.nifi.components.PropertyDescriptor;
import org.apache.nifi.expression.ExpressionLanguageScope;
import org.apache.nifi.flowfile.FlowFile;
import org.apache.nifi.processor.*;
import org.apache.nifi.processor.exception.ProcessException;
import org.apache.commons.io.IOUtils;
import org.apache.nifi.processor.io.InputStreamCallback;
import org.apache.nifi.processor.io.OutputStreamCallback;
import org.apache.nifi.processor.util.StandardValidators;
import org.json.JSONObject;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.*;
import java.util.concurrent.atomic.AtomicReference;

@Tags({"JSON","WLOG","Read","CSV","Flat JSON"})
@CapabilityDescription("Custom Processor that handle WLOG JSON Files")

public class HandleWLOGJSON extends AbstractProcessor {

    private final static String REGEX ="\\[|\\]";


    public static final PropertyDescriptor COLUMNS_JSON_FIELD = new PropertyDescriptor
            .Builder().name("columns")
            .displayName("JSON key item where the columns names are")
            .description("JSON key item where the columns names are")
            .required(true)
            .expressionLanguageSupported(ExpressionLanguageScope.FLOWFILE_ATTRIBUTES)
            .addValidator(StandardValidators.NON_EMPTY_VALIDATOR)
            .build();

    public static final PropertyDescriptor DATA_JSON_FIELD = new PropertyDescriptor
            .Builder().name("data")
            .displayName("JSON key item where the array of data arrays are")
            .description("JSON key item where the array of data arrays are")
            .required(true)
            .expressionLanguageSupported(ExpressionLanguageScope.FLOWFILE_ATTRIBUTES)
            .addValidator(StandardValidators.NON_EMPTY_VALIDATOR)
            .build();

    private static final Relationship SUCCESS = new Relationship.Builder()
            .name("success")
            .description("JSON flattened to csv")
            .build();

    private static final Relationship FAILURE = new Relationship.Builder()
            .name("failure")
            .description("JSON content that could not be processed")
            .build();

    private Set<Relationship> relationships;

    private List<PropertyDescriptor> descriptors;

    @Override
    public Set<Relationship> getRelationships() {
        return this.relationships;
    }

    @Override
    public final List<PropertyDescriptor> getSupportedPropertyDescriptors() {
        return descriptors;
    }


    @Override
    protected void init(final ProcessorInitializationContext context) {

        final List<PropertyDescriptor> descriptors = new ArrayList<PropertyDescriptor>();
        descriptors.add(COLUMNS_JSON_FIELD);
        descriptors.add(DATA_JSON_FIELD);
        this.descriptors = Collections.unmodifiableList(descriptors);

        final Set<Relationship> relationships = new HashSet<Relationship>();
        relationships.add(SUCCESS);
        relationships.add(FAILURE);

        this.relationships = Collections.unmodifiableSet(relationships);
    }

    @Override
    public void onTrigger(ProcessContext context, ProcessSession session) throws ProcessException {

        final AtomicReference<String> value = new AtomicReference<>();

        FlowFile flowFile = session.get();
        if ( flowFile == null ) {
            return;
        }

        final String columnsJSONFieldKey = context.getProperty(COLUMNS_JSON_FIELD).evaluateAttributeExpressions(flowFile).getValue().toUpperCase();
        final String dataJSONFieldKey = context.getProperty(DATA_JSON_FIELD).evaluateAttributeExpressions(flowFile).getValue().toUpperCase();


        try {
            session.read(flowFile, new InputStreamCallback() {
                @Override
                public void process(InputStream inputStream) throws IOException {
                    String jsonToCsv = handleWLOGJSON(inputStream,columnsJSONFieldKey,dataJSONFieldKey);
                    value.set(jsonToCsv);
                }
            });
        }catch (Exception e){

            getLogger().error("Failed to process incoming JSON file. " + e.getMessage(), e);
            FlowFile failedFlowFile = session.putAttribute(flowFile,
                    HandleWLOGJSON.class.getName() + ".error", e.getMessage());
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

    private String handleWLOGJSON(InputStream inputStream, String columnsJSONFieldKey, String dataJSONFieldKey)  {

        StringBuilder csvToString = new StringBuilder();
        try{
            String json = IOUtils.toString(inputStream);

            JSONObject jsonObject = new org.json.JSONObject(json);

            List<Object> columns=jsonObject.getJSONArray(columnsJSONFieldKey).toList();
            Optional<String> columnsOptional =columns.stream().map(Object::toString).reduce( (x, y) -> x.concat(","+y));
            String headerString = columnsOptional.get();
            csvToString.append(headerString+"\n");

            List<Object> data=jsonObject.getJSONArray(dataJSONFieldKey).toList();

            Optional<String>  dataOptional = data.stream().map( x -> {
                String row =x.toString().replaceAll(REGEX,"");
                int indexLastComa = row.lastIndexOf(",");
                char[] rowChars = row.toCharArray();
                rowChars[indexLastComa] = '-';
                String rowClean = String.valueOf(rowChars);
                return rowClean;
            }).reduce( (x, y) -> x.concat("\n"+y));

            String dataString = dataOptional.get();
            csvToString.append(dataString);

        }catch(Exception ex){
            ex.printStackTrace();
        }
        finally {
            try {
                if(inputStream != null)
                    inputStream.close();
            } catch (IOException e) {
                e.printStackTrace();
                getLogger().error("Failed to close " + e.getMessage(), e);
            }
        }
        return csvToString.toString();
    }
}
