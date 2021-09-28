import { Component } from '@angular/core';
import { FormControl } from '@angular/forms';
import { Observable } from 'rxjs';
import { startWith, map, debounceTime } from 'rxjs/operators';
import { Staedte } from './staedte';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  stadtInput = new FormControl()
  title = 'SweetGeeks'
  filteredStaedte: Observable<String[]> = this.stadtInput.valueChanges.pipe(
    startWith(''),
    map(stadt => stadt ? this._filter(stadt) : Staedte.slice())
  )

  private _filter(name: string): String[] {
    const filterValue = name.toLowerCase();
    return Staedte.filter(option => option.toLowerCase().includes(filterValue));
  }

  submitting() {
    console.log('HEYYY!!')
  }
}
