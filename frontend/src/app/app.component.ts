import { Component, ElementRef, OnInit, ViewChild } from '@angular/core'
import { FormControl, FormBuilder, FormGroup } from '@angular/forms'
import { combineLatest, Observable, of, throwError } from 'rxjs'
import { startWith, map, skipWhile, tap, catchError } from 'rxjs/operators'
import { Staedte } from './staedte'
import { HttpClient } from '@angular/common/http'
import { trigger, transition, style, animate } from '@angular/animations'
import { environment } from 'src/environments/environment'

export interface alldata {
  buildings: building[]
  gesamtkwh?: number
  co2Einsparung?: number
  kostenEinsparung?: number
  gesamtVerbrauch?: number
  anteil?: number
}
export interface building {
  adresse: string
  anzahl_0: string
  kw_17: number
  kwh_kwp: string
  modarea: string
  name: string
  radabs: string
  str_17: number
  type: string
}

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
  animations: [
    trigger('inOutAnimation', [
      transition(':enter', [
        style({ height: 0, opacity: 0 }),
        animate('1s ease-out', style({ height: 300, opacity: 1 })),
      ]),
      transition(':leave', [
        style({ height: 300, opacity: 1 }),
        animate('1s ease-in', style({ height: 0, opacity: 0 })),
      ]),
    ]),
  ],
})
export class AppComponent implements OnInit {
  @ViewChild('container') container: ElementRef | undefined
  @ViewChild('solarFacts') solarFacts: ElementRef | undefined
  stadtInput = new FormControl()
  filters: string[] = []
  formGroup: FormGroup = this.fb.group({
    schooling: true,
    kindergarten: true,
    security: true,
    government: true,
  })
  toggleType = new FormControl(', []')
  title = 'SweetGeeks'

  filteredStaedte$: Observable<String[]> = this.stadtInput.valueChanges.pipe(
    startWith(''),
    skipWhile((v) => v.length < 1),
    map((stadt) => (stadt ? this._filter(stadt) : Staedte.slice()))
  )
  apiError: boolean = false
  constructor(private http: HttpClient, private fb: FormBuilder) {}
  httpAnswer$: Observable<alldata> | undefined
  selectedStadt = ''

  ngOnInit(): void {}

  umlauteUmschreiben(word: string): string {
    return word.toLowerCase().replace('ä', 'ae').replace('ü', 'ue').replace('ö', 'oe')
  }

  keypressed(event: KeyboardEvent) {
    if (event.key == "Enter") {
      this.onSelectStadt()
    }
  }

  private _filter(name: string): String[] {
    const filterValue = name.toLowerCase()
    return Staedte.filter((option) => option.toLowerCase().includes(filterValue))
  }

  onSelectStadt() {
    this.selectedStadt = this.umlauteUmschreiben(this.stadtInput.value)
    this.apiError = false
    this.httpAnswer$ = this.apiCall(this.selectedStadt)
    this.cssAnimation()
  }

  ngOnDestroy(): void {}

  apiCall(stadt: string, filter?: string[]): Observable<alldata> | undefined {
    if (!Staedte.includes(this.stadtInput.value)) {
      throw new Error("Not a valid city was selected");
    }
    const callBuildings$ = this.http.get(environment.BACK_END_ADDRESS + `/getBuildings?cityName=${stadt.toLowerCase()}`)
    const v$ = this.formGroup.valueChanges.pipe(
      startWith({
        schooling: true,
        kindergarten: true,
        security: true,
        government: true,
      })
    )
    return combineLatest([callBuildings$, v$]).pipe(
      catchError(err => {
        this.apiError = true;
        return throwError(err);
      }),
      map(([res, filter]: any) => {
        const buildings = res.filter((b: building) => filter[b.type])
        const data: alldata = {
          buildings: buildings,
        }
        data.gesamtkwh = this.berechnetGesamtKwha(buildings)
        data.kostenEinsparung = data.gesamtkwh * 0.31
        data.co2Einsparung = (data.gesamtkwh * 366) / 1000 / 1000
        const callCityDetails$ = this.http.get(environment.BACK_END_ADDRESS + `/getCityDetails?cityName=${stadt.toLowerCase()}`).toPromise()
        .then(res  => {
          console.log(res)
         
            
            
    
        });
        
      console.log(callCityDetails$)
        if(stadt.toLowerCase() == 'grevenbroich') data.gesamtVerbrauch = 513 // TODO: API CALL
        if(stadt.toLowerCase() == 'juechen') data.gesamtVerbrauch = 188
        data.anteil = this.anteilAnGesamtVerbrauch(data.gesamtVerbrauch as number, data.gesamtkwh)
        return data
      }),
    ) as Observable<alldata>
  }

  cssAnimation() {
    const divEl: HTMLDivElement = this.container?.nativeElement
    divEl.style.justifyContent = 'flex-start'
    divEl.style.marginTop = '2rem'
  }

  anteilAnGesamtVerbrauch(gesamtVerbrauch: number, potential: number): number {
    return potential / 1000 / gesamtVerbrauch
  } 

  berechnetGesamtKwha(buildings: building[], filters?: string[]): number {
    return buildings.reduce(
      (prev: building, curr: any) => {
        return { ...curr, str_17: prev.str_17 + curr.str_17 }
      },
      { str_17: 0 } as building
    ).str_17
  }
}
