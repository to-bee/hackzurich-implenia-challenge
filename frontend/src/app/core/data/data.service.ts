import {Injectable} from '@angular/core';
import {BehaviorSubject, Observable, ReplaySubject, tap} from 'rxjs';
import {HttpClient} from '@angular/common/http';
import {
    CaseDetail,
    CaseRead,
    CaseService,
    Configuration,
} from '../../../openapi-generated';
import {environment} from 'app/@environments/environment';
import {RecordService} from "../../../openapi-generated/api/record.service";
import {CaseRecordUpdateOutput} from "../../../openapi-generated/model/caseRecordUpdateOutput";
import {data} from "autoprefixer";
import {ActivatedRoute} from "@angular/router";
import {QuestionService} from "../../../openapi-generated/api/question.service";
import {SaveQuestionApiQuestionsPostRequestParams} from "../../../openapi-generated/api/question.serviceInterface";

@Injectable({
    providedIn: 'root',
})
export class DataService {
    private questionService: QuestionService;
    private recordService: RecordService;
    private caseService: CaseService;

    private _cases: BehaviorSubject<CaseRead[] | null> = new BehaviorSubject(null);
    private _case: ReplaySubject<CaseDetail | null> = new ReplaySubject(1, 1500);


    get cases(): Observable<CaseRead[] | null> {
        return this._cases.asObservable();
    }


    get case(): Observable<CaseDetail> {
        return this._case.asObservable();
    }

    constructor(private http: HttpClient, private route: ActivatedRoute) {
        this.questionService = new QuestionService(
            this.http,
            environment.serverUrl,
            new Configuration({basePath: environment.serverUrl}),
        );
        this.recordService = new RecordService(
            this.http,
            environment.serverUrl,
            new Configuration({basePath: environment.serverUrl}),
        );
        this.caseService = new CaseService(
            this.http,
            environment.serverUrl,
            new Configuration({basePath: environment.serverUrl}),
        );
    }

    getAllCases(status?: string): Observable<CaseRead[]> {
        return this.caseService.askQuestionApiCasesGet({status}, 'body').pipe(
            tap((cases) => {
                console.error(cases)
                this._cases.next(cases);
            }),
        );
    }

    getCaseById(id: string): Observable<any> {

        return this.caseService.readCaseByIdApiCasesIdGet({id}, 'body')
            .pipe(
                tap((value) => {
                    this._case.next(value);
                })
            );
    }

    updateRecord(
        caseId: number,
        recordId: number,
        data: { [key: string]: any } | null,
    ): Observable<CaseRecordUpdateOutput> {
        return this.recordService.updateRecordApiCasesCaseIdRecordsRecordIdPut({
            caseId,
            recordId,
            requestBody: data,
        });
    }

    createRecord(
        caseId: number,
        data: { [key: string]: any } | null,
    ): Observable<CaseRecordUpdateOutput> {
        return this.recordService.createRecordApiCasesCaseIdRecordsPost({
            caseId,
            requestBody: data,
        });
    }

    saveQuestions(
        data: SaveQuestionApiQuestionsPostRequestParams,
    ): Observable<any> {
        return this.questionService.saveQuestionApiQuestionsPost(data);
    }

    readQuestionsApiQuestionsGet(params: any) {
        return this.questionService
            .readQuestionsApiQuestionsGet(params.id, true, {})
            .subscribe((value) => {
                return value;
            });
    }
}
