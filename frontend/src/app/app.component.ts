import { Component, ElementRef, ViewChild } from '@angular/core';
import { FormControl } from '@angular/forms';
import { Observable } from 'rxjs';
import { startWith, map, skip, skipWhile, tap } from 'rxjs/operators';
import { Staedte } from './staedte';
import { HttpClient } from '@angular/common/http'
import { trigger, transition, style, animate } from '@angular/animations';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
  animations: [
    trigger(
      'inOutAnimation',
      [
        transition(
          ':enter',
          [
            style({ height: 0, opacity: 0 }),
            animate('1s ease-out',
                    style({ height: 300, opacity: 1 }))
          ]
        ),
        transition(
          ':leave',
          [
            style({ height: 300, opacity: 1 }),
            animate('1s ease-in',
                    style({ height: 0, opacity: 0 }))
          ]
        )
      ]
    )
  ]
})
export class AppComponent {
  @ViewChild('container') container: ElementRef | undefined
  @ViewChild('solarFacts') solarFacts: ElementRef | undefined
  stadtInput = new FormControl()
  title = 'SweetGeeks'
  filteredStaedte: Observable<String[]> = this.stadtInput.valueChanges.pipe(
    startWith(''),
    skipWhile(v => v.length < 1),
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
    this.http.get(`http://192.168.178.50/api/?cityName=${stadt}`).pipe(
      tap(res => console.log(res))
    )
  }

  cssAnimation() {
    const divEl: HTMLDivElement = this.container?.nativeElement
    divEl.style.justifyContent = 'flex-start'
    divEl.style.marginTop = '2rem'
    // divEl.style.transform = 'translateY(-4rem)'
    const ansEl: HTMLDivElement = this.solarFacts?.nativeElement
    ansEl.style.opacity = '1'
  }

  reset() {
    this.antwortIstDa = false
    this.stadtInput.reset()
  }
}
