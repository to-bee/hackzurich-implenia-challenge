import {AfterViewInit, Component, OnDestroy, OnInit} from '@angular/core';
import {CommonModule} from '@angular/common';
import {MatButtonModule} from "@angular/material/button";
import {MatCheckboxModule} from "@angular/material/checkbox";
import {MatFormFieldModule} from "@angular/material/form-field";
import {MatIconModule} from "@angular/material/icon";
import {MatInputModule} from "@angular/material/input";
import {MatOptionModule, MatRippleModule} from "@angular/material/core";
import {MatSelectModule} from "@angular/material/select";
import {MatSlideToggleModule} from "@angular/material/slide-toggle";
import {FormControl, FormGroup, ReactiveFormsModule, UntypedFormBuilder, Validators} from "@angular/forms";
import {
    CaseDetail,
    CaseRead,
    CaseStatus,
    CaseType, CountryCode,
    Currency, Division,
    ProcessingStatus
} from "../../../../../../../openapi-generated";
import {MatDatepickerModule} from "@angular/material/datepicker";
import {DataService} from "../../../../../../core/data/data.service";
import {ActivatedRoute} from "@angular/router";
import {tap} from "rxjs";
import {error} from "@angular/compiler-cli/src/transformers/util";

@Component({
    selector: 'hack-case-details',
    standalone: true,
    imports: [CommonModule, MatButtonModule, MatCheckboxModule, MatFormFieldModule, MatIconModule, MatInputModule, MatOptionModule, MatRippleModule, MatSelectModule, MatSlideToggleModule, ReactiveFormsModule, MatDatepickerModule],
    templateUrl: './case-details.component.html',
    styleUrls: ['./case-details.component.scss']
})
export class CaseDetailsComponent implements OnInit, AfterViewInit, OnDestroy {

    case: CaseDetail;
    dataHasLoaded = false;

    divisions: Division[] = [
        "BUILDINGS",
        "CIVIL",
        "REAL_ESTATE",
        "SPECIAL_FOUNDATIONS",
        "TUNNELING"
    ]
    caseDetailForm: FormGroup;
    caseTypes: CaseType[] = ["ACTIVE",
        "EXPECTED_ACTIVE",
        "PASSIVE",
        "EXPECTED_PASSIVE"];

    caseStatis: CaseStatus[] = [
        'ACTIVE',
        'ON_HOLD',
        'CLOSED'
    ]

    currencies: Currency[] = [
        "CHF",
        "EURO",
        "USD"
    ]
    processingStatis: ProcessingStatus[] = [
        'FIRST_INSTANCE_EXCHANGE_OF_BRIEFS',
        'FIRST_INSTANCE_COURT_DELIBERATION',
        'EVIDENCE_PRESERVATION_PROCEEDINGS',
        'SECOND_INSTANCE_EXCHANGE_OF_BRIEFS',
        'BANKRUPTCY_PROCEEDINGS',
        'SECOND_INSTANCE_COURT_DELIBERATION',
        'CONCILIATION_ADR_PROCEEDINGS'
    ]

    countryCodes: CountryCode[] = [
        "CH",
        "DE",
        "AT",
        "IT",
        "FR",
        "US",
        "RO",
        "NO",
        "SE"

    ]


    constructor(private _formBuilder: UntypedFormBuilder, private _dataService: DataService, private route: ActivatedRoute) {
        // this.dataHasLoaded = true;

        this.setupForm();


    }

    setupForm() {
        this.caseDetailForm = this._formBuilder.group({
            id: [{value: '', disabled: true}, Validators.required],
            case_number: ['', Validators.required],
            business_unit: ['', Validators.required],
            division: ['', Validators.required],
            ic: ['', Validators.required],
            investment_center_name: ['', Validators.required],
            psp: ['', Validators.required],
            project_on_rda: ['', Validators.required],
            legal_responsible: ['', Validators.required],
            finance_responsible: ['', Validators.required],
            expected_legal_costs: ['', Validators.required],
            accumulated_legal_costs: ['', Validators.required],
            accumulated_court_costs: ['', Validators.required],
            expected_court_costs: ['', Validators.required],
            start_date_proceeding: ['', Validators.required],
            end_date_proceeding: ['', Validators.required],
            interest_date: ['', Validators.required],
            implenia_share_percent: ['', Validators.required],
            project_description: ['', Validators.required],
            case_type: ['', Validators.required],//CaseType
            responsible: ['', Validators.required],
            real_case: ['', Validators.required],
            opportunities_risks: ['', Validators.required],
            // accumulated_costs: ['', Validators.required],
            interest_rate_percent: ['', Validators.required],
            case_status: ['', Validators.required],
            value_in_dispute: ['', Validators.required],
            currency: ['', Validators.required],//Type
            subject_matter: ['', Validators.required],
            status_proceeding: ['', Validators.required],//ProcessingStatus
            country_party_relation: ['', Validators.required],//CountryCode
            claimant_respondent: ['', Validators.required],//ClaimantRespondant
            review_status: ['', Validators.required] //ReviewStatus
        })
    }

    ngOnInit(): void {
        this.route.paramMap.subscribe(params => {
            let id = params.get('id');
            this._dataService.getCaseById(id).subscribe(
                value => {
                    this.case = value;
                    console.warn(this.case)
                    // this.setupForm();
                    this.dataHasLoaded = true;
                    this.caseDetailForm.get('id').patchValue(this.case.current.id);
                    this.caseDetailForm.get('case_number').patchValue(this.case.current.case_number);
                    this.caseDetailForm.get('subject_matter').patchValue(this.case.current.subject_matter);
                    this.caseDetailForm.get('case_status').patchValue(this.case.current.case_status);
                    this.caseDetailForm.get('business_unit').patchValue(this.case.current.business_unit);
                    this.caseDetailForm.get('division').patchValue(this.case.current.division);
                    this.caseDetailForm.get('ic').patchValue(this.case.current.ic);
                    this.caseDetailForm.get('investment_center_name').patchValue(this.case.current.investment_center_name);
                    this.caseDetailForm.get('psp').patchValue(this.case.current.psp);
                    this.caseDetailForm.get('project_on_rda').patchValue(this.case.current.project_on_rda);
                    this.caseDetailForm.get('legal_responsible').patchValue(this.case.current.legal_responsible);
                    this.caseDetailForm.get('finance_responsible').patchValue(this.case.current.finance_responsible);
                    this.caseDetailForm.get('expected_legal_costs').patchValue(this.case.current.expected_legal_costs);
                    this.caseDetailForm.get('accumulated_legal_costs').patchValue(this.case.current.accumulated_legal_costs);
                    this.caseDetailForm.get('accumulated_court_costs').patchValue(this.case.current.accumulated_court_costs);
                    this.caseDetailForm.get('expected_court_costs').patchValue(this.case.current.expected_court_costs);
                    this.caseDetailForm.get('start_date_proceeding').patchValue(this.case.current.start_date_proceeding);
                    this.caseDetailForm.get('end_date_proceeding').patchValue(this.case.current.end_date_proceeding);
                    this.caseDetailForm.get('interest_date').patchValue(this.case.current.interest_date);
                    this.caseDetailForm.get('implenia_share_percent').patchValue(this.case.current.implenia_share_percent);
                    this.caseDetailForm.get('project_description').patchValue(this.case.current.project_description);
                    this.caseDetailForm.get('case_type').patchValue(this.case.current.case_type);
                    this.caseDetailForm.get('responsible').patchValue(this.case.current.responsible);
                    this.caseDetailForm.get('currency').patchValue(this.case.current.currency);
                    this.caseDetailForm.get('status_proceeding').patchValue(this.case.current.status_proceeding);
                    this.caseDetailForm.get('value_in_dispute').patchValue(this.case.current.value_in_dispute);
                    this.caseDetailForm.get('interest_rate_percent').patchValue(this.case.current.interest_rate_percent);
                    this.caseDetailForm.get('opportunities_risks').patchValue(this.case.current.opportunities_risks);
                    // this.caseDetailForm.get('accumulated_costs').patchValue(this.case.current.accumulated_costs);
                    this.caseDetailForm.get('real_case').patchValue(this.case.current.real_case);
                }
            )
        })

        // this.caseDetailForm.get('id').patchValue(this.case.current.id);
        // this.caseDetailForm.get('id').disable();
    }

    updateSelectedProduct(): void {
        console.error(this.caseDetailForm.errors);
        console.warn(this.case);
        if(this.caseDetailForm.invalid){
            return;
        }
        this._dataService.createRecord(this.case.current.id,this.case);
    }

    ngAfterViewInit(): void {
    }

    ngOnDestroy(): void {
    }


}
