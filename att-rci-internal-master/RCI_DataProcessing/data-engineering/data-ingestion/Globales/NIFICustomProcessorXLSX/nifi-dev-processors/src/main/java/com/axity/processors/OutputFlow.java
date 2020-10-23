/**
 * 
 */
package com.axity.processors;

import org.apache.nifi.util.StringUtils;

/**
 * @author EludDeJesúsCárcamo
 *
 */
public class OutputFlow {

	private String fileProcess;
	private String fileRejected;

	/**
	 * @param the fileProcess and fileRejected
	 */
	public OutputFlow(String fileProcess, String fileRejected) {
		super();
		this.fileProcess = fileProcess;
		this.fileRejected = fileRejected;
	}
		
	/**
	 * 
	 */
	public OutputFlow() {
		fileProcess=StringUtils.EMPTY;
		fileRejected=StringUtils.EMPTY;
	}



	/**
	 * @return the fileProcess
	 */
	public String getFileProcess() {
		return fileProcess;
	}

	/**
	 * @param fileProcess the fileProcess to set
	 */
	public void setFileProcess(String fileProcess) {
		this.fileProcess = fileProcess;
	}

	/**
	 * @return the fileRejected
	 */
	public String getFileRejected() {
		return fileRejected;
	}

	/**
	 * @param fileRejected the fileRejected to set
	 */
	public void setFileRejected(String fileRejected) {
		this.fileRejected = fileRejected;
	}

}
