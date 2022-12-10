import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

def simulation(fixed, variable):
    infected = [fixed['initial_infections']]
    new_infections = [fixed['initial_infections']]
    total_infections = fixed['initial_infections']

    for t in range(fixed['duration']):
        cur_infections = infected[-1]
        # remove people who are no longer contagious
        if len(new_infections) > fixed['days_spreading']:
            cur_infections -= new_infections[-fixed['days_spreading'] - 1]
        # if social distancing, change number of daily contacts
        if t >= variable['red_start'] and t < variable['red_end']:
            daily_contacts = variable['red_daily_contacts']
        else:
            daily_contacts = fixed['init_contacts']
        # compute number of new cases
        total_contacts = cur_infections * daily_contacts
        susceptible = fixed['pop'] - total_infections
        risky_contacts = total_contacts * (susceptible/fixed['pop'])
        newly_infected = round(risky_contacts * fixed['contagiousness'])
        # update variables
        new_infections.append(newly_infected)
        total_infections += newly_infected
        infected.append(cur_infections + newly_infected)

    return infected, total_infections

def plot_infection(infections, total_infections, fixed):
    infection_plot = plt.plot(infections, 'r', label = 'Infected')[0]
    plt.xticks(fontsize = 'large')
    plt.yticks(fontsize = 'large')
    plt.xlabel('Days Since First Infection', fontsize='xx-large')
    plt.ylabel('Number Currently Infected', fontsize='xx-large')
    plt.title('Number of Infections Assuming No Vaccine\n' +
              f'Pop = {fixed["pop"]:,}, ' +
              f'Contacts/Day = {fixed["init_contacts"]}, ' +
              f'Infectivity = {(100*fixed["contagiousness"]):.1f}%, ' +
              f'Days Contagious = {fixed["days_spreading"]}',
              fontsize='xx-large')
    plt.legend(fontsize='xx-large')
    txt_box = plt.text(plt.xlim()[1]/2, plt.ylim()[1]/1.25,
                       f'Total Infections = {total_infections:,.0f}',
                       fontdict={'size':'xx-large', 'weight':'bold',
                                 'color':'red'})
    return infection_plot, txt_box

fixed = {
    'pop': 5000000,  # population at risk
    'duration': 500,  # number of days for simulation
    'initial_infections': 4,  # initial number of cases
    'init_contacts': 50,  # contacts without social distancing
    'contagiousness': 0.005,  # prob. of getting disease if exposed
    'days_spreading': 10}  # days contagious after infection
variable = {
    #  'red_daily_contacts': 4,  # social distancing
    'red_daily_contacts': fixed['init_contacts'],  # social distancing
    'red_start': 20,  # start of social distancing
    'red_end': 200}  # end of social distancing

#  infections, total_infections = simulation(fixed, variable)
fig = plt.figure(figsize=(12, 8.5))
infections_ax = plt.axes([0.12, 0.2, 0.8, 0.65])
contacts_ax = plt.axes([0.25, 0.09, 0.65, 0.03])
start_ax = plt.axes([0.25, 0.06, 0.65, 0.03])
end_ax = plt.axes([0.25, 0.03, 0.65, 0.03])

contacts_slider = Slider(
    contacts_ax,  # axes object containing the slider
    'reduced\ncontacts/day',  # name of slider
    0,  # minimal value of the parameter
    50,  # maximal value of the parameter
    50)  # initial value of the parameter
contacts_slider.label.set_fontsize(12)
start_day_slider = Slider(start_ax, 'start reduction', 1,
                          30, 20)
start_day_slider.label.set_fontsize(12)
end_day_slider = Slider(end_ax, 'end reduction', 30,
                          400, 200)
end_day_slider.label.set_fontsize(12)

def update(fixed, infection_plot, txt_box,
           contacts_slider, start_day_slider,
           end_day_slider):
    variable = {'red_daily_contacts': contacts_slider.val,
                'red_start': start_day_slider.val,
                'red_end': end_day_slider.val}
    I, total_infections = simulation(fixed, variable)
    infection_plot.set_ydata(I)  # new y-coordinates for plot
    txt_box.set_text(f'Total Infections = {total_infections:,.0f}')

slider_update = lambda _: update(fixed, infection_plot,
                                 txt_box, contacts_slider,
                                 start_day_slider,
                                 end_day_slider)
contacts_slider.on_changed(slider_update)
start_day_slider.on_changed(slider_update)
end_day_slider.on_changed(slider_update)

infections, total_infections = simulation(fixed, variable)
plt.axes(infections_ax)
infection_plot, txt_box = plot_infection(infections, total_infections, fixed)
plt.show()


