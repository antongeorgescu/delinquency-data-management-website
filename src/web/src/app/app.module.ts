import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { RouterModule } from '@angular/router';

import { AppComponent } from './app.component';
import { HomeComponent } from './components/home/home.component';
import { UserProfilesComponent } from './components/user-profiles/user-profiles.component';
import { LoanInfoComponent } from './components/loan-info/loan-info.component';
import { ProgramsComponent } from './components/programs/programs.component';
import { LoanPaymentsComponent } from './components/loan-payments/loan-payments.component';
import { DataService } from './services/data.service';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    UserProfilesComponent,
    LoanInfoComponent,
    ProgramsComponent,
    LoanPaymentsComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    RouterModule.forRoot([
      { path: '', component: HomeComponent },
      { path: 'users', component: UserProfilesComponent },
      { path: 'loans', component: LoanInfoComponent },
      { path: 'programs', component: ProgramsComponent },
      { path: 'payments', component: LoanPaymentsComponent },
      { path: '**', redirectTo: '' }
    ])
  ],
  providers: [DataService],
  bootstrap: [AppComponent]
})
export class AppModule { }