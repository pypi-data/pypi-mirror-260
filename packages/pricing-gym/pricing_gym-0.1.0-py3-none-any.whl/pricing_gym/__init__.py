from gymnasium.envs.registration import register

register(
    id='pricing_gym/ToyPricing-v0',
    entry_point='pricing_gym.envs:ToyPricing',
    max_episode_steps=12500,
)

register(
    id='pricing_gym/Pricing-v0',
    entry_point='pricing_gym.envs:Pricing',
    max_episode_steps=12500,
)