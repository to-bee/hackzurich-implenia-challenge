import {inject} from '@angular/core';
import {Routes} from '@angular/router';
import {InventoryService} from 'app/modules/admin/apps/ecommerce/inventory/inventory.service';
import {CaseListComponent} from "./inventory/list/case-list.component";
import {CaseComponent} from "./inventory/case.component";
import {CaseDetailsComponent} from "./inventory/case-details/case-details.component";
import {DataService} from "../../../../core/data/data.service";

export default [
    {
        path: '',
        pathMatch: 'full',
        redirectTo: 'inventory',
    },
    {
        path: 'inventory',
        component: CaseComponent,
        children: [
            {
                path: ':id',
                component: CaseDetailsComponent,
                resolve: {
                    // id: () => inject(DataService).getCaseById()
                }
            },
            {
                path: '',
                component: CaseListComponent,
                resolve: {
                    cases: () => inject(DataService).getAllCases(),
                },
            },


        ],
    },

] as Routes;
