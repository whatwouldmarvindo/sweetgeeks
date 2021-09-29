import { Component, ElementRef, OnInit, ViewChild } from '@angular/core'
import { FormControl, FormBuilder, FormGroup, Validators } from '@angular/forms'
import { Observable } from 'rxjs'
import { startWith, map, skipWhile, tap } from 'rxjs/operators'
import { Staedte } from './staedte'
import { HttpClient } from '@angular/common/http'
import { trigger, transition, style, animate } from '@angular/animations'

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
  tglBildung = true
  tglKindergarten = true
  tglSicherheit = true
  formGroup: FormGroup = this.fb.group({
    tglBildung: 'true',
    tglKindergarten: 'true',
    tglSicherheit: 'true'
  });
  toggleType = new FormControl(', []')
  title = 'SweetGeeks'
  filteredStaedte: Observable<String[]> = this.stadtInput.valueChanges.pipe(
    startWith(''),
    skipWhile((v) => v.length < 1),
    map((stadt) => (stadt ? this._filter(stadt) : Staedte.slice()))
    )
    constructor(private http: HttpClient, private fb: FormBuilder) {
  
    }
  httpAnswer$: Observable<alldata> | undefined
  selectedStadt = ''


  ngOnInit(): void {

  }

  onTypeSelectSubmit() {
    this.selectedStadt = this.stadtInput.value
    var filters = []
    
    if(!this.formGroup.controls['tglBildung'].value) filters.push("schooling")
    if(!this.formGroup.controls['tglKindergarten'].value) filters.push("kindergarten")
    if(!this.formGroup.controls['tglSicherheit'].value) filters.push("security")

    this.httpAnswer$ = this.apiCall(this.selectedStadt.toLowerCase(),filters)
  }

  private _filter(name: string): String[] {
    const filterValue = name.toLowerCase()
    return Staedte.filter((option) => option.toLowerCase().includes(filterValue))
  }

  onSelectItem() {
    this.selectedStadt = this.stadtInput.value
    this.httpAnswer$ = this.apiCall(this.selectedStadt.toLowerCase())
    this.cssAnimation()
  }


 ngOnDestroy():void {

}

  apiCall(stadt: string, filter?:string[]) {
    return this.http.get(`http://192.168.178.50:5000/api?cityName=${stadt.toLowerCase()}`).pipe(
      map((res: any) => {
        const data: alldata = {
          buildings: res
        }
        data.gesamtkwh = this.berechnetGesamtKwha(res)
        data.kostenEinsparung = data.gesamtkwh * 0.31
        data.co2Einsparung = (data.gesamtkwh * 366) / 1000 / 1000
        data.gesamtVerbrauch = 513
        data.anteil = this.anteilAnGesamtVerbrauch(data.gesamtVerbrauch, data.gesamtkwh)
        //Hier am besten ne Filterfunktion nehmen, war zu müde :D
    
        if(filter) {
          console.log("Filter: ")
          console.log(filter)
          var builds = []
          for(var build of data.buildings){
            if (!(build.type in filter)) builds.push(build)
          }
          data.buildings = builds
        }
        console.log(data.buildings[0].type)
        return data
      })
    ) as Observable<alldata>
  }

  cssAnimation() {
    const divEl: HTMLDivElement = this.container?.nativeElement
    divEl.style.justifyContent = 'flex-start'
    divEl.style.marginTop = '2rem'
  }

  anteilAnGesamtVerbrauch(gesamtVerbrauch: number, potential: number): number {
    console.log(gesamtVerbrauch, potential)
    return potential / 1000 / gesamtVerbrauch
  }

  berechnetGesamtKwha(buildings: building[], filters?: string[]): number {
    return buildings.reduce((prev: building, curr: any) => {
      return { ...curr, str_17: prev.str_17 + curr.str_17 }
    }).str_17
  }
}
