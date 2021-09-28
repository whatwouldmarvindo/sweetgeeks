import { Component, ElementRef, ViewChild } from '@angular/core';
import { FormControl } from '@angular/forms';
import { Observable } from 'rxjs';
import { startWith, map, skip, skipWhile, tap } from 'rxjs/operators';
import { Staedte } from './staedte';
import { HttpClient, HttpHeaders } from '@angular/common/http'

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent {
  @ViewChild('container') container: ElementRef | undefined
  @ViewChild('solarFacts') solarFacts: ElementRef | undefined
  stadtInput = new FormControl()
  title = 'SweetGeeks'
  filteredStaedte: Observable<String[]> = this.stadtInput.valueChanges.pipe(
    startWith(''),
    skipWhile(v => v.length < 3),
    map(stadt => stadt ? this._filter(stadt) : Staedte.slice())
  )
  antwortIstDa = false
  selectedStadt = ''

  constructor(private http: HttpClient) {}

  private _filter(name: string): String[] {
    const filterValue = name.toLowerCase();
    return Staedte.filter(option => option.toLowerCase().includes(filterValue));
  }

  onSelectItem() {
    this.selectedStadt = this.stadtInput.value
    this.apiCall(this.selectedStadt)
    this.antwortIstDa = true
    this.cssAnimation()
  }

  apiCall(stadt: string) {
    this.http.get(`http://192.168.178.50/api/${stadt}`).pipe(
      tap(res => console.log(res))
    )
  }

  cssAnimation() {
    const divEl: HTMLDivElement = this.container?.nativeElement
    divEl.style.transition = '1s'
    divEl.style.transform = 'translateY(-20vh)'
    const ansEl: HTMLDivElement = this.solarFacts?.nativeElement
    ansEl.style.opacity = '1'
  }

  reset() {
    this.antwortIstDa = false
    this.stadtInput.reset()
  }
}
