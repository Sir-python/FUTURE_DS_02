import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def plot_monthly_ticket_volume(df):
    monthly = (
        df.groupby("Month-Year of Purchase")
            .agg(
                ticket_count = ("Ticket ID", "count"), 
                avg_response_hrs = ("First Response Hrs", "mean")
        ).reset_index()
    )
    fig, ax1 = plt.subplots(figsize=(12, 8))
    # Plot Ticket Count
    ax1.plot(
        monthly['Month-Year of Purchase'],
        monthly['ticket_count'],
        marker='o', markersize=8, linewidth=2,
        label='Ticket Count'
    )
    ax1.set_xlabel('Month-Year', fontsize=12)
    ax1.set_ylabel('Ticket Count', fontsize=12)
    ax1.tick_params(axis='x', labelrotation=45, labelsize=10)
    ax1.tick_params(axis='y', labelsize=10)

    ax2 = ax1.twinx()
    ax2.plot(
        monthly['Month-Year of Purchase'],
        monthly['avg_response_hrs'],
        marker='s', markersize=8, linewidth=2,
        linestyle='--', color='orange',
        label='Avg First Response (hrs)'
    )
    # Title and legend
    plt.title('Monthly Ticket Volume & Avg First Response', fontsize=14)
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

    plt.tight_layout()
    plt.show()

def plot_ticket_volume(df):
    by_channel = (
        df.groupby("Ticket Channel").agg
            (
                ticket_count = ("Ticket ID", "count"),
                avg_response_hrs = ("First Response Hrs", "mean")
            ).reset_index()
    )
    channels = by_channel["Ticket Channel"]
    counts   = by_channel['ticket_count']
    avgresp  = by_channel['avg_response_hrs']

    x = np.arange(len(channels))
    width = 0.6

    # First figure: Ticket Count
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    ax1.bar(x, counts, width=width, color='green')
    ax1.set_xticks(x)
    ax1.set_xticklabels(channels)
    ax1.set_ylabel("Ticket Count")
    ax1.set_title("Ticket Volume by Channel")
    ax1.grid(True, which='major', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

    # Second figure: Avg First Response
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    ax2.bar(x, avgresp, width=width, color='orange')
    ax2.set_xticks(x)
    ax2.set_xticklabels(channels)
    ax2.set_ylabel("Avg First Response (hrs)")
    ax2.set_title("Avg First Response Time by Channel")
    ax2.grid(True, which='major', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

def issue_category_frequency(df):
    frequency_df = (df.groupby("Ticket Subject").agg(ticket_count = ("Ticket ID", "count")).reset_index().sort_values(by="ticket_count", ascending=False))
    colors = sns.color_palette("flare", len(frequency_df))
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(frequency_df['Ticket Subject'], frequency_df['ticket_count'], color=colors)
    ax.invert_yaxis()
    ax.set_xlabel('Ticket Count')
    ax.set_title('Top Issue Categories')
    plt.tight_layout()
    plt.show()

def csat_distribution(df):
    csat_df = df[["Resolution Hrs", "Customer Satisfaction Rating"]].dropna()
    csat_df.columns = ["resolution_hrs", "csat"]
    
    plt.figure(figsize=(10,5))
    sns.boxplot(
        data=csat_df,
        x="resolution_hrs",
        y="csat",
        orient="h",
        color="skyblue",
        medianprops={
            "color": "orange",
            "linewidth": 2
        },
        whiskerprops={"color": "black"},
        boxprops={"edgecolor": "black"},
        capprops={"color": "black"}
    )
    plt.xlabel("Customer Satisfaction Rating")
    plt.ylabel("Time to Resolution (hrs)")
    plt.title("Resolution Time Distribution by CSAT")
    plt.tight_layout()
    plt.show()

def ticket_by_gender(df):
    gender_counts = df.groupby("Customer Gender")["Ticket ID"].count()
    explode = [0.05 if count == gender_counts.max() else 0 for count in gender_counts]
    colors = sns.color_palette("Set2", n_colors=len(gender_counts))
    
    fig, ax = plt.subplots(figsize=(4, 4))
    pie_result = ax.pie(
        gender_counts,
        labels=gender_counts.index,
        autopct='%1.1f%%',
        startangle=140,
        explode=explode,
        colors=colors,
        shadow=True,
        pctdistance=0.6,
        labeldistance=1.1
    )
    if len(pie_result) == 3:
        patches, texts, autotexts = pie_result
    else:
        patches, texts = pie_result
        autotexts = []

    for t in texts:
        t.set_color('black')
        t.set_fontsize(10)

    for at in autotexts:
        at.set_color('white')
        at.set_fontweight('bold')
        at.set_fontsize(11)

    plt.title("Ticket Volume by Gender")
    plt.tight_layout()
    plt.show()
    
def root_cause_heatmap(df):
    heatmap_df = (df.groupby(["Ticket Subject", "Ticket Type"]).size().unstack(fill_value=0))
    plt.figure(figsize=(12, 6))
    sns.heatmap(
        heatmap_df,
        annot=True,        
        fmt="d",           
        cmap="YlOrRd",     # color palette
        linewidths=0.5,
        linecolor='gray'
    )

    plt.title("Root Cause Frequency by Ticket Type")
    plt.ylabel("Root Cause")
    plt.xlabel("Ticket Type")
    plt.tight_layout()
    plt.show()