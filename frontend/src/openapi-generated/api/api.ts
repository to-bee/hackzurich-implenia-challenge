export * from './analytics.service';
import { AnalyticsService } from './analytics.service';
export * from './analytics.serviceInterface';
export * from './case.service';
import { CaseService } from './case.service';
export * from './case.serviceInterface';
export const APIS = [AnalyticsService, CaseService];
