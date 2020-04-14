import pandas as pd

url = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv"
states = pd.read_csv(url, usecols=[0, 3, 12], index_col=['denominazione_regione', 'data'], parse_dates=['data'],
                         squeeze=True).sort_index()
new_cases = states.xs("Campania").rename("Campania cases")

print(new_cases["data"])
#print([d.strftime('%-d %b') for d in new_cases['data']])











def plot_rt(result, ax, state_name):
    ax.set_title(f"{state_name}")

    # Colors
    ABOVE = [1, 0, 0]
    MIDDLE = [1, 1, 1]
    BELOW = [0, 0, 0]
    cmap = ListedColormap(np.r_[
                              np.linspace(BELOW, MIDDLE, 25),
                              np.linspace(MIDDLE, ABOVE, 25)
                          ])
    color_mapped = lambda y: np.clip(y, .5, 1.5) - .5

    index =  result['ML'].index.get_level_values('data')
    values = result['ML'].values

    # Plot dots and line
    ax.plot(index, values, c='k', zorder=1, alpha=.25)
    ax.scatter(index,
               values,
               s=40,
               lw=.5,
               c=cmap(color_mapped(values)),
               edgecolors='k', zorder=2)

    # Aesthetically, extrapolate credible interval by 1 day either side
    lowfn = interp1d(date2num(index),
                     result['Low'].values,
                     bounds_error=False,
                     fill_value='extrapolate')

    highfn = interp1d(date2num(index),
                      result['High'].values,
                      bounds_error=False,
                      fill_value='extrapolate')

    extended = pd.date_range(start=pd.Timestamp('2020-03-01'),
                             end=index[-1] + pd.Timedelta(days=1))

    ax.fill_between(extended,
                    lowfn(date2num(extended)),
                    highfn(date2num(extended)),
                    color='k',
                    alpha=.1,
                    lw=0,
                    zorder=3)

    ax.axhline(1.0, c='k', lw=1, label='$R_t=1.0$', alpha=.25);

    # Formatting
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    ax.xaxis.set_minor_locator(mdates.DayLocator())

    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.1f}"))
    ax.yaxis.tick_right()
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.margins(0)
    ax.grid(which='major', axis='y', c='k', alpha=.1, zorder=-2)
    ax.margins(0)
    ax.set_ylim(0.0, 3.5)
    ax.set_xlim(pd.Timestamp('2020-03-01'), result.index.get_level_values('data')[-1] + pd.Timedelta(days=1))
    fig.set_facecolor('w')




