import { LOCALE_ID, NgModule } from '@angular/core'
import { BrowserModule } from '@angular/platform-browser'

import { AppComponent } from './app.component'
import { BrowserAnimationsModule } from '@angular/platform-browser/animations'
import { ReactiveFormsModule } from '@angular/forms'
import { MatInputModule } from '@angular/material/input'
import { MatFormFieldModule } from '@angular/material/form-field'
import { MatSlideToggleModule } from '@angular/material/slide-toggle'
import { MatButtonModule } from '@angular/material/button'
import { MatAutocompleteModule } from '@angular/material/autocomplete'
import { HttpClientModule } from '@angular/common/http'
import { registerLocaleData } from '@angular/common'
import localeDe from '@angular/common/locales/de'
import { Utf8Pipe } from './utf8.pipe'
import { MatExpansionModule } from '@angular/material/expansion'

registerLocaleData(localeDe)

@NgModule({
  declarations: [AppComponent, Utf8Pipe],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    ReactiveFormsModule,
    MatInputModule,
    MatFormFieldModule,
    MatButtonModule,
    MatAutocompleteModule,
    MatSlideToggleModule,
    HttpClientModule,
    MatExpansionModule
  ],
  providers: [{ provide: LOCALE_ID, useValue: 'de-DE' }],
  bootstrap: [AppComponent],
})
export class AppModule {}
