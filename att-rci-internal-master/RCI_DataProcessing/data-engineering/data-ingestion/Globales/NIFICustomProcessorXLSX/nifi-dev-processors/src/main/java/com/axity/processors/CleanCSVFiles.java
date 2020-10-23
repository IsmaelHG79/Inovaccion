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

/**
 * @author EludDeJesúsCárcamo
 *
 */
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.text.MessageFormat;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Scanner;
import java.util.Set;
import java.util.concurrent.atomic.AtomicReference;

import org.apache.nifi.annotation.behavior.WritesAttribute;
import org.apache.nifi.annotation.behavior.WritesAttributes;
import org.apache.nifi.annotation.documentation.CapabilityDescription;
import org.apache.nifi.annotation.documentation.Tags;
import org.apache.nifi.annotation.lifecycle.OnScheduled;
import org.apache.nifi.components.PropertyDescriptor;
import org.apache.nifi.expression.ExpressionLanguageScope;
import org.apache.nifi.flowfile.FlowFile;
import org.apache.nifi.flowfile.attributes.CoreAttributes;
import org.apache.nifi.processor.AbstractProcessor;
import org.apache.nifi.processor.ProcessContext;
import org.apache.nifi.processor.ProcessSession;
import org.apache.nifi.processor.ProcessorInitializationContext;
import org.apache.nifi.processor.Relationship;
import org.apache.nifi.processor.exception.ProcessException;
import org.apache.nifi.processor.io.InputStreamCallback;
import org.apache.nifi.processor.io.OutputStreamCallback;
import org.apache.nifi.processor.util.StandardValidators;

@Tags({"Clean","CSV","TXT"})
@CapabilityDescription("Custom Processor that clean header.")
@WritesAttributes({
    @WritesAttribute(attribute = "filename", description = "The filename is set to the name of the file on disk")})
public class CleanCSVFiles extends AbstractProcessor {


    public static final PropertyDescriptor CSV_SEPARATOR = new PropertyDescriptor
            .Builder().name("csv-split-separator")
            .displayName("Tag Split Separator of CSV Files")
            .description("Character to separate csv file")
            .required(true)
            .expressionLanguageSupported(ExpressionLanguageScope.FLOWFILE_ATTRIBUTES)
            .addValidator(StandardValidators.NON_EMPTY_VALIDATOR)
            .build();

    private static final Relationship SUCCESS = new Relationship.Builder()
            .name("success")
            .description("CSV parsed")
            .build();

    private static final Relationship REJECTED = new Relationship.Builder()
            .name("rejected")
            .description("CSV rejected")
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
        descriptors.add(CSV_SEPARATOR);
        this.descriptors = Collections.unmodifiableList(descriptors);

        final Set<Relationship> relationships = new HashSet<Relationship>();
        relationships.add(SUCCESS);
        relationships.add(REJECTED);
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

    @OnScheduled
    public void onScheduled(final ProcessContext context) {
    }

    @Override
    public void onTrigger(final ProcessContext context, final ProcessSession session) throws ProcessException {
		
		final AtomicReference<String> value_process = new AtomicReference<>();
		final AtomicReference<String> value_rejected = new AtomicReference<>();
		FlowFile flowFile = session.get();
		if ( flowFile == null ) {
			return;
		}
		
        // get values
        final String csvSeparator = context.getProperty(CSV_SEPARATOR).evaluateAttributeExpressions(flowFile).getValue();

        try {
            session.read(flowFile, new InputStreamCallback() {
                @Override
                public void process(InputStream inputStream) throws IOException {
                	OutputFlow response = startClean(inputStream,csvSeparator);
                	value_process.set(response.getFileProcess());
                	value_rejected.set(response.getFileRejected());
                }
            });
        }catch (Exception e){
            getLogger().error("Failed to process incoming Excel document. " + e.getMessage(), e);
            FlowFile failedFlowFile = session.putAttribute(flowFile,
                    CleanCSVFiles.class.getName() + ".error", e.getMessage());
            session.transfer(failedFlowFile, FAILURE);
        }
		
        String results_process = value_process.get();
        if(results_process != null && !results_process.isEmpty()){
            flowFile = session.putAttribute( flowFile, "mime.type", "text/csv" );
            flowFile = session.putAttribute(flowFile, "csv", results_process);
        }
        
        flowFile = session.write(flowFile, new OutputStreamCallback() {
            @Override
            public void process(OutputStream out) throws IOException {
                out.write(value_process.get().getBytes());
            }
        });
        
        FlowFile flowFile_rejected = session.create();
        String results_rejected = value_rejected.get();
        if(results_rejected != null && !results_rejected.isEmpty()){
        	flowFile_rejected = session.putAttribute(flowFile_rejected, CoreAttributes.FILENAME.key(), flowFile.getAttribute(CoreAttributes.FILENAME.key()).concat("_rejected"));
        	flowFile_rejected = session.putAttribute(flowFile_rejected, "mime.type", "text/csv" );
        	flowFile_rejected = session.putAttribute(flowFile_rejected, "csv", results_rejected);
        }
        
        flowFile_rejected = session.write(flowFile_rejected, new OutputStreamCallback() {
            @Override
            public void process(OutputStream out) throws IOException {
                out.write(value_rejected.get().getBytes());
            }
        });
        
        session.transfer(flowFile, SUCCESS);
        session.transfer(flowFile_rejected, REJECTED);
    }
	
    private static String cleanHeader(String valueHeader) {
        String normalizer = Normalizer.normalize(valueHeader, Normalizer.Form.NFD).replaceAll("[^\\p{ASCII}]", "");
        String withoutSpace = normalizer.trim().replace(" ","_");
        String cleaned = withoutSpace.replaceAll("[{}()/]+","").replace("#","Num");
        return cleaned;
    }

    private OutputFlow startClean(final InputStream inputStream, final String csvSeparator) {
    	Scanner inputFile = null;
    	OutputFlow res = new OutputFlow();
    	
        try {
			//input
            inputFile = new Scanner(inputStream);
            String firstLine = inputFile.nextLine();
            String headerFile []= firstLine.split(csvSeparator);
            
			//output
            String newpFile=cleanHeader(firstLine ) + "\n";
            
			//rejected
            String newRejectedFile=cleanHeader(firstLine) + "\n";

            while (inputFile.hasNextLine()) {
                String line = inputFile.nextLine();
                String rowColumnFile []= line.split(csvSeparator);
                if (headerFile.length == rowColumnFile.length) {
                	newpFile = newpFile.concat(line + "\n");
                }
                else
                	newRejectedFile = newRejectedFile.concat(line + "\n");
            }
            
            res = new OutputFlow(newpFile, newRejectedFile);
        } catch (Exception ex) {
        	getLogger().error(MessageFormat.format("Error: {0}", ex.getMessage()));
            ex.printStackTrace();
        } finally {
        		if(inputFile != null) {
        			inputFile.close();
        		}
        }
        return res;
    }
}
