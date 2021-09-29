import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'utf8'
})
export class Utf8Pipe implements PipeTransform {

  transform(value: string): string {
    value = value.replace('Ã¤', 'ä')
    value = value.replace('Ã¤', 'ä')
    value = value.replace('Ã¶', 'ö')
    value = value.replace('Ã¼', 'ü')
    return value;
  }

}
