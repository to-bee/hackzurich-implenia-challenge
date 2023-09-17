import {AsyncPipe, CurrencyPipe, NgClass, NgFor, NgIf, NgSwitchDefault, NgTemplateOutlet} from '@angular/common';
import {
    AfterViewInit,
    ChangeDetectionStrategy,
    ChangeDetectorRef,
    Component,
    OnDestroy,
    OnInit,
    ViewChild,
    ViewEncapsulation
} from '@angular/core';
import {FormsModule, ReactiveFormsModule, UntypedFormBuilder, UntypedFormControl,} from '@angular/forms';
import {MatButtonModule} from '@angular/material/button';
import {MatCheckboxModule} from '@angular/material/checkbox';
import {MatOptionModule, MatRippleModule} from '@angular/material/core';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatIconModule} from '@angular/material/icon';
import {MatInputModule} from '@angular/material/input';
import {MatPaginator, MatPaginatorModule} from '@angular/material/paginator';
import {MatProgressBarModule} from '@angular/material/progress-bar';
import {MatSelectModule} from '@angular/material/select';
import {MatSlideToggleModule} from '@angular/material/slide-toggle';
import {MatSort, MatSortModule} from '@angular/material/sort';
import {fuseAnimations} from '@fuse/animations';
import {FuseConfirmationService} from '@fuse/services/confirmation';
import {InventoryService} from 'app/modules/admin/apps/ecommerce/inventory/inventory.service';
import {debounceTime, map, Observable, Subject, switchMap, takeUntil} from 'rxjs';
import {InventoryPagination} from "../case.types";
import {DataService} from "../../../../../../core/data/data.service";
import {CaseRead} from "../../../../../../../openapi-generated";
import {ActivatedRoute, Router, RouterLink} from "@angular/router";

@Component({
    selector: 'case-list',
    templateUrl: './case-list.component.html',
    styles: [
        /* language=SCSS */
        `
          .inventory-grid {
            grid-template-columns: 48px auto 40px;

            @screen sm {
              grid-template-columns: 48px auto 112px 72px;
            }

            @screen md {
              grid-template-columns: 48px 112px auto 112px 72px;
            }

            @screen lg {
              grid-template-columns: 48px 112px auto 112px 96px 96px 72px;
            }
          }
        `,
    ],
    encapsulation: ViewEncapsulation.None,
    changeDetection: ChangeDetectionStrategy.OnPush,
    animations: fuseAnimations,
    standalone: true,
    imports: [NgIf, MatProgressBarModule, MatFormFieldModule, MatIconModule, MatInputModule, FormsModule, ReactiveFormsModule, MatButtonModule, MatSortModule, NgFor, NgTemplateOutlet, MatPaginatorModule, NgClass, MatSlideToggleModule, MatSelectModule, MatOptionModule, MatCheckboxModule, MatRippleModule, AsyncPipe, CurrencyPipe, RouterLink, NgSwitchDefault],
})
export class CaseListComponent implements OnInit, AfterViewInit, OnDestroy {
    @ViewChild(MatPaginator) private _paginator: MatPaginator;
    @ViewChild(MatSort) private _sort: MatSort;

    cases$: Observable<CaseRead[]>;
    cases: CaseRead[];

    flashMessage: 'success' | 'error' | null = null;
    isLoading: boolean = false;
    pagination: InventoryPagination;
    searchInputControl: UntypedFormControl = new UntypedFormControl();
    tagsEditMode: boolean = false;
    private _unsubscribeAll: Subject<any> = new Subject<any>();

    /**
     * Constructor
     */
    constructor(
        private _changeDetectorRef: ChangeDetectorRef,
        private _fuseConfirmationService: FuseConfirmationService,
        private _formBuilder: UntypedFormBuilder,
        private _inventoryService: InventoryService,
        private _dataService: DataService,
        private router: Router,
        private route: ActivatedRoute
    ) {
    }

    // -----------------------------------------------------------------------------------------------------
    // @ Lifecycle hooks
    // -----------------------------------------------------------------------------------------------------

    /**
     * On init
     */
    ngOnInit(): void {
        this._dataService.getAllCases()
            .pipe(takeUntil(this._unsubscribeAll))
            .subscribe((cases: CaseRead[]) => {
                // Update the brands
                this.cases = cases;
                // Mark for check
                this._changeDetectorRef.markForCheck();
            });
        this.cases$ = this._dataService.cases;

        // Subscribe to search input field value changes
        this.searchInputControl.valueChanges
            .pipe(
                takeUntil(this._unsubscribeAll),
                debounceTime(300),
                switchMap((query) => {
                    this.isLoading = true;
                    return this._inventoryService.getProducts(0, 10, 'name', 'asc', query);
                }),
                map(() => {
                    this.isLoading = false;
                }),
            )
            .subscribe();
    }

    /**
     * After view init
     */
    ngAfterViewInit(): void {
    }

    /**
     * On destroy
     */
    ngOnDestroy(): void {
        // Unsubscribe from all subscriptions
        this._unsubscribeAll.next(null);
        this._unsubscribeAll.complete();
    }

    // -----------------------------------------------------------------------------------------------------
    // @ Public methods
    // -----------------------------------------------------------------------------------------------------

    createProduct(): void {
        // Create the product
        // this._dataService.subscribe((newProduct) => {
        //     // Go to new product
        //
        //     // Fill the form
        //
        //     // Mark for check
        //     this._changeDetectorRef.markForCheck();
        // });
        console.error('please implement')
    }

    /**
     * Toggle the tags edit mode
     */
    toggleTagsEditMode(): void {
        this.tagsEditMode = !this.tagsEditMode;
    }

    /**
     * Show flash message
     */
    showFlashMessage(type: 'success' | 'error'): void {
        // Show the message
        this.flashMessage = type;

        // Mark for check
        this._changeDetectorRef.markForCheck();

        // Hide it after 3 seconds
        setTimeout(() => {
            this.flashMessage = null;

            // Mark for check
            this._changeDetectorRef.markForCheck();
        }, 3000);
    }

    /**
     * Track by function for ngFor loops
     *
     * @param index
     * @param item
     */
    trackByFn(index: number, item: any): any {
        return item.id || index;
    }
}
