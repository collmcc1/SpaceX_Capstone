{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "fc44defb",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Import required libraries\n",
    "import pandas as pd\n",
    "import dash\n",
    "from dash import html\n",
    "from dash import dcc\n",
    "from dash.dependencies import Input, Output\n",
    "import plotly.express as px"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "ab4bb406",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Read the airline data into pandas dataframe\n",
    "spacex_df = pd.read_csv(\"spacex_launch_dash.csv\")\n",
    "max_payload = spacex_df['Payload Mass (kg)'].max()\n",
    "min_payload = spacex_df['Payload Mass (kg)'].min()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "ab3544c9",
   "metadata": {},
   "outputs": [],
   "source": [
    "#print(spacex_df['Launch Site'].unique())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "03122669",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Create a dash application\n",
    "app = dash.Dash(__name__)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "9b3c055b",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Create an app layout\n",
    "app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',\n",
    "                                        style={'textAlign': 'center', 'color': '#503D36',\n",
    "                                               'font-size': 40}),\n",
    "                                 # TASK 1: Add a dropdown list to enable Launch Site selection\n",
    "                                # The default select value is for ALL sites\n",
    "                                dcc.Dropdown(id='site-dropdown',\n",
    "                                             options=[\n",
    "                                                    {'label': 'All Sites', 'value': 'ALL'},\n",
    "                                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},\n",
    "                                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},\n",
    "                                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},\n",
    "                                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}],\n",
    "                                             value='ALL',\n",
    "                                             placeholder=\"State\",\n",
    "                                             searchable=True\n",
    "                                            ),\n",
    "                                html.Br(),\n",
    "                                \n",
    "                                # TASK 2: Add a pie chart to show the total successful launches count for all sites\n",
    "                                # If a specific launch site was selected, show the Success vs. Failed counts for the site\n",
    "                                html.Div(dcc.Graph(id='success-pie-chart')),\n",
    "                                html.Br(),\n",
    "\n",
    "                                html.P(\"Payload range (Kg):\"),\n",
    "                                # TASK 3: Add a slider to select payload range\n",
    "                                dcc.RangeSlider(id='payload-slider',\n",
    "                                                min=0, max=10000, step=1000,\n",
    "                                                marks={0: '0', 100: '100'},\n",
    "                                                value=[min_payload, max_payload]),\n",
    "\n",
    "                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success\n",
    "                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),\n",
    "                                ])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "056fa46b",
   "metadata": {},
   "outputs": [],
   "source": [
    "# TASK 2:\n",
    "# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output\n",
    "# Function decorator to specify function input and output\n",
    "@app.callback(Output(component_id='success-pie-chart', component_property='figure'),\n",
    "              Input(component_id='site-dropdown', component_property='value'))\n",
    "def get_pie_chart(entered_site):    \n",
    "    if entered_site == 'ALL':\n",
    "        fig = px.pie(spacex_df, \n",
    "                     values='class', \n",
    "                     names='Launch Site', \n",
    "                     title='Total Success Launches By Site')        \n",
    "    else:\n",
    "        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]\n",
    "        filtered_df = filtered_df.groupby('class').count().reset_index()        \n",
    "        fig = px.pie(filtered_df, \n",
    "                     values='Unnamed: 0', \n",
    "                     names='class', \n",
    "                     title='Total Launches for site {}'.format(entered_site))        \n",
    "        # return the outcomes piechart for a selected site\n",
    "    return fig"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "68876aa7",
   "metadata": {},
   "outputs": [],
   "source": [
    "# TASK 4:\n",
    "# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output\n",
    "@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),\n",
    "              Input(component_id='site-dropdown', component_property='value'), \n",
    "              Input(component_id=\"payload-slider\", component_property=\"value\"))\n",
    "def get_scatter_chart(entered_site, payload_range):\n",
    "    print('Params: {} {}'.format(entered_site, payload_range))\n",
    "    if entered_site == 'ALL':\n",
    "        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= int(payload_range[0])) &\n",
    "                                (spacex_df['Payload Mass (kg)'] <= int(payload_range[1]))\n",
    "                               ]\n",
    "        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='All sites - payload mass between {:8,d}kg and {:8,d}kg'.format(int(payload_range[0]),int(payload_range[1])))\n",
    "    else:\n",
    "        filtered_df = spacex_df[(spacex_df['Launch Site'] == entered_site) & \n",
    "                                (spacex_df['Payload Mass (kg)'] >= int(payload_range[0])) &\n",
    "                                (spacex_df['Payload Mass (kg)'] <= int(payload_range[1]))\n",
    "                               ]\n",
    "        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Site {} - payload mass between {:8,d}kg and {:8,d}kg'.format(entered_site,int(payload_range[0]),int(payload_range[1])))\n",
    "    \n",
    "    return fig"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "id": "76590145",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Dash is running on http://127.0.0.1:8050/\n",
      "\n",
      "Dash is running on http://127.0.0.1:8050/\n",
      "\n",
      " * Serving Flask app \"__main__\" (lazy loading)\n",
      " * Environment: production\n",
      "\u001b[31m   WARNING: This is a development server. Do not use it in a production deployment.\u001b[0m\n",
      "\u001b[2m   Use a production WSGI server instead.\u001b[0m\n",
      " * Debug mode: on\n"
     ]
    },
    {
     "ename": "OSError",
     "evalue": "[Errno 48] Address already in use",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mOSError\u001b[0m                                   Traceback (most recent call last)",
      "\u001b[0;32m/var/folders/66/mljtxj297435fmz3ylbhl9fw0000gn/T/ipykernel_22183/161386266.py\u001b[0m in \u001b[0;36m<module>\u001b[0;34m\u001b[0m\n\u001b[1;32m      1\u001b[0m \u001b[0;31m# Run the app\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      2\u001b[0m \u001b[0;32mif\u001b[0m \u001b[0m__name__\u001b[0m \u001b[0;34m==\u001b[0m \u001b[0;34m'__main__'\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m----> 3\u001b[0;31m     \u001b[0mapp\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mrun_server\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mdebug\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0;32mTrue\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m",
      "\u001b[0;32m~/opt/anaconda3/lib/python3.9/site-packages/dash/dash.py\u001b[0m in \u001b[0;36mrun_server\u001b[0;34m(self, host, port, proxy, debug, dev_tools_ui, dev_tools_props_check, dev_tools_serve_dev_bundles, dev_tools_hot_reload, dev_tools_hot_reload_interval, dev_tools_hot_reload_watch_interval, dev_tools_hot_reload_max_retry, dev_tools_silence_routes_logging, dev_tools_prune_errors, **flask_run_options)\u001b[0m\n\u001b[1;32m   2076\u001b[0m                     \u001b[0mextra_files\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mappend\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mpath\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m   2077\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m-> 2078\u001b[0;31m         \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mserver\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mrun\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mhost\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mhost\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mport\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mport\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mdebug\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mdebug\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;34m**\u001b[0m\u001b[0mflask_run_options\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m",
      "\u001b[0;32m~/opt/anaconda3/lib/python3.9/site-packages/flask/app.py\u001b[0m in \u001b[0;36mrun\u001b[0;34m(self, host, port, debug, load_dotenv, **options)\u001b[0m\n\u001b[1;32m    988\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    989\u001b[0m         \u001b[0;32mtry\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 990\u001b[0;31m             \u001b[0mrun_simple\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mhost\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mport\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mself\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;34m**\u001b[0m\u001b[0moptions\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    991\u001b[0m         \u001b[0;32mfinally\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    992\u001b[0m             \u001b[0;31m# reset the first request information if the development server\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;32m~/opt/anaconda3/lib/python3.9/site-packages/werkzeug/serving.py\u001b[0m in \u001b[0;36mrun_simple\u001b[0;34m(hostname, port, application, use_reloader, use_debugger, use_evalex, extra_files, exclude_patterns, reloader_interval, reloader_type, threaded, processes, request_handler, static_files, passthrough_errors, ssl_context)\u001b[0m\n\u001b[1;32m    982\u001b[0m             \u001b[0ms\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0msocket\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0msocket\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0maddress_family\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0msocket\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mSOCK_STREAM\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    983\u001b[0m             \u001b[0ms\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0msetsockopt\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0msocket\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mSOL_SOCKET\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0msocket\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mSO_REUSEADDR\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;36m1\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 984\u001b[0;31m             \u001b[0ms\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mbind\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mserver_address\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    985\u001b[0m             \u001b[0ms\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mset_inheritable\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;32mTrue\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    986\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;31mOSError\u001b[0m: [Errno 48] Address already in use"
     ]
    }
   ],
   "source": [
    "# Run the app\n",
    "if __name__ == '__main__':\n",
    "    app.run_server(debug=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "38aa50d5",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
