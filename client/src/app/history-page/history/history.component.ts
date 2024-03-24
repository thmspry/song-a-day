import {Component, OnInit} from '@angular/core';
import { ajax } from "rxjs/ajax";
import { Song } from "../../model/Song";
import {SongCardComponent} from "../song-card/song-card.component";
import {Observable, switchMap, tap} from "rxjs";

@Component({
  selector: 'app-history',
  standalone: true,
  imports: [
    SongCardComponent
  ],
  templateUrl: './history.component.html',
  styleUrl: './history.component.scss'
})
export class HistoryComponent implements OnInit {
  protected historySongs: Song[] | undefined;

  ngOnInit(): void {
    this.getHistory$().subscribe();
  }

  private getHistory$(): Observable<Song[]> {
    return ajax.getJSON<Song[]>('http://127.0.0.1:8000/api/history').pipe(tap((songs: Song[]) => {
      this.historySongs = songs;
    }));
  }

  protected clearHistory() {
    ajax.delete('http://127.0.0.1:8000/api/history').pipe(switchMap(() => this.getHistory$())).subscribe();
  }
}
