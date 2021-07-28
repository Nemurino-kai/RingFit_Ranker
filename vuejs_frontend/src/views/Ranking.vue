<template>
  <div class="ranking container">
    <h2 >Exercise Ranking</h2> <div class="text-muted">({{dailyRank.start_day}} 04:00:00 ～ {{dailyRank.stop_day}} 03:59:59)</div>
<br>

<div>
  <label>集計期間&nbsp;</label>
  <b-button variant="primary" to="/" size="sm">Daily</b-button>
  <b-button variant="outline-primary" to="/monthly" size="sm">Monthly</b-button>
</div>

    <hr style="margin-top:0.5em;margin-bottom:1em;">

    <form class="form-group form-inline">
      <label for="aggregated day">集計日&nbsp;</label>
      <Datepicker v-model="defaultDate" :disabled-dates="dailyRank.disabledDates" id="aggregated day"></Datepicker>
    </form>
    <p class="mt-3" v-if='dailyRank.errored'>データを読み込めませんでした。ページを更新し直すか、時間をおいて再びアクセスしてください。</p>
  <div class="overflow-auto" v-if="rows != 0">
    <b-pagination
      v-model="currentPage"
      :total-rows="rows"
      :per-page="perPage"
      aria-controls="exercise-table"
      align="center"
    ></b-pagination>
      <b-table striped hover caption-top
      id="exercise-table"
          :items="dailyRank.exercise_data"
          :fields="columns"
          :per-page="perPage"
          :current-page="currentPage"
          small
    ></b-table>
        <b-pagination
      v-model="currentPage"
      :total-rows="rows"
      :per-page="perPage"
      @page-click="goTop"
      aria-controls="exercise-table"
      align="center"
    ></b-pagination>
    <p class="mt-3" style="text-align:center;">displaying <b>{{(currentPage-1)* 100 + 1}} - {{Math.min(currentPage* 100, rows)}}</b> records in total <b>{{rows}}</b></p>
  </div>

</div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  data () {
    return {
      currentPage: 1,
      perPage: 100,
      columns: [ {
        label: 'Rank',
        key: 'ranking',
        sortable: true
      },
      {
        label: 'Username',
        key: 'user_name',
        sortable: true
      },
      {
        label: 'kcal',
        key: 'kcal',
        sortable: true
      },
      {
        label: 'Date',
        key: 'tweeted_time',
        sortable: true
      }]
    }
  },
  methods: {
    goTop: function () {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      })
    }
  },
  created () {
    // データが無ければ、集計する
    if (this.$store.state.dailyRank.exercise_data.length === 0) {
      this.$store.dispatch('dailyRank/search', this.$moment().subtract(4, 'hours').format('YYYY-MM-DD'))
    }
  },
  computed: {
    ...mapState(['dailyRank']),
    rows () {
      return this.$store.state.dailyRank.exercise_data.length
    },
    defaultDate: {
      get () { return this.$store.state.dailyRank.defaultDate },
      set (value) {
        this.$store.dispatch('dailyRank/search', this.$moment(value).format('YYYY-MM-DD'))
        this.currentPage = 1
      }
    }

  }
}
</script>
