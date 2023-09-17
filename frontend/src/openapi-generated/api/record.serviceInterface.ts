/**
 * FastAPI
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 0.1.0
 *
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */
import { HttpHeaders }                                       from '@angular/common/http';

import { Observable }                                        from 'rxjs';

import { HTTPValidationError } from '../model/models';


import { Configuration }                                     from '../configuration';
import {CaseRecordUpdateOutput} from "../model/caseRecordUpdateOutput";


export interface CreateRecordApiCasesCaseIdRecordsPostRequestParams {
    caseId: any;
    requestBody: { [key: string]: any; } | null;
}

export interface UpdateRecordApiCasesCaseIdRecordsRecordIdPutRequestParams {
    caseId: any;
    recordId: any;
    requestBody: { [key: string]: any; } | null;
}


export interface RecordServiceInterface {
    defaultHeaders: HttpHeaders;
    configuration: Configuration;

    /**
     * Create Record
     *
* @param requestParameters
     */
    createRecordApiCasesCaseIdRecordsPost(requestParameters: CreateRecordApiCasesCaseIdRecordsPostRequestParams, extraHttpRequestParams?: any): Observable<any>;

    /**
     * Update Record
     *
* @param requestParameters
     */
    updateRecordApiCasesCaseIdRecordsRecordIdPut(requestParameters: UpdateRecordApiCasesCaseIdRecordsRecordIdPutRequestParams, extraHttpRequestParams?: any): Observable<CaseRecordUpdateOutput>;

}
