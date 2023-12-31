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
import {HttpHeaders} from '@angular/common/http';

import {Observable} from 'rxjs';

import {CaseCreate} from '../model/models';
import {CaseDetail} from '../model/models';
import {CaseStatus} from '../model/models';
import {HTTPValidationError} from '../model/models';


import {Configuration} from '../configuration';


export interface ApproveCaseApiCasesIdApprovePutRequestParams {
    id: any;
}

export interface AskQuestionApiCasesGetRequestParams {
    status?: any;
}

export interface CreateCaseApiCasesPostRequestParams {
    requestBody: { [key: string]: any; } | null;
}

export interface DeclineCaseApiCasesIdDeclinePutRequestParams {
    id: any;
}

export interface ReadCaseByIdApiCasesIdGetRequestParams {
    id: any;
}

export interface ReadCasesApiCasesAskGetRequestParams {
    question: any;
}

export interface ReadFileApiCasesImportFilePostRequestParams {
    file: any | null;
}

export interface ReadTextApiCasesImportTextPostRequestParams {
    rawData: any;
}


export interface CaseServiceInterface {
    defaultHeaders: HttpHeaders;
    configuration: Configuration;

    /**
     * Approve Case
     *
     * @param requestParameters
     */
    approveCaseApiCasesIdApprovePut(requestParameters: ApproveCaseApiCasesIdApprovePutRequestParams, extraHttpRequestParams?: any): Observable<any>;

    /**
     * Ask Question
     *
     * @param requestParameters
     */
    askQuestionApiCasesGet(requestParameters: AskQuestionApiCasesGetRequestParams, extraHttpRequestParams?: any): Observable<any>;

    /**
     * Create Case
     *
     * @param requestParameters
     */
    createCaseApiCasesPost(requestParameters: CreateCaseApiCasesPostRequestParams, extraHttpRequestParams?: any): Observable<any>;

    /**
     * Decline Case
     *
     * @param requestParameters
     */
    declineCaseApiCasesIdDeclinePut(requestParameters: DeclineCaseApiCasesIdDeclinePutRequestParams, extraHttpRequestParams?: any): Observable<any>;

    /**
     * Read Case By Id
     *
     * @param requestParameters
     */
    readCaseByIdApiCasesIdGet(requestParameters: ReadCaseByIdApiCasesIdGetRequestParams, extraHttpRequestParams?: any): Observable<CaseDetail>;

    /**
     * Read Cases
     *
     * @param requestParameters
     */
    readCasesApiCasesAskGet(requestParameters: ReadCasesApiCasesAskGetRequestParams, extraHttpRequestParams?: any): Observable<any>;

    /**
     * Read File
     *
     * @param requestParameters
     */
    readFileApiCasesImportFilePost(requestParameters: ReadFileApiCasesImportFilePostRequestParams, extraHttpRequestParams?: any): Observable<any>;

    /**
     * Read Text
     *
     * @param requestParameters
     */
    readTextApiCasesImportTextPost(requestParameters: ReadTextApiCasesImportTextPostRequestParams, extraHttpRequestParams?: any): Observable<any>;

}
