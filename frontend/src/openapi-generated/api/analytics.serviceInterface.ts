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

import {HTTPValidationError} from '../model/models';
import {MetabaseTheme} from '../model/models';


import {Configuration} from '../configuration';


export interface GetMetabaseUrlApiMetabaseQuestionIdGetRequestParams {
    questionId: any;
    type?: any;
    startDate?: any | null;
    endDate?: any | null;
    theme?: any;
}


export interface AnalyticsServiceInterface {
    defaultHeaders: HttpHeaders;
    configuration: Configuration;

    /**
     * Get Metabase Url
     *
     * @param requestParameters
     */
    getMetabaseUrlApiMetabaseQuestionIdGet(requestParameters: GetMetabaseUrlApiMetabaseQuestionIdGetRequestParams, extraHttpRequestParams?: any): Observable<any>;

}
